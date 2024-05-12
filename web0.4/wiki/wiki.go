package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"regexp"
)

const (
	PAGESDIR = "./pages/"
	USERSDIR = "./users/"
	FILESEXT = ".json"
)

type Page struct {
	Title   string        `json:"title"`
	Body    template.HTML `json:"body"`
	Private bool          `json:"private"`
}

func (p *Page) save() error {
	filename := p.Title + FILESEXT
	data, err := json.Marshal(p)
	if err != nil {
		return err
	}
	return os.WriteFile(PAGESDIR+filename, data, 0600)
}

func loadPage(title string) (*Page, error) {
	filename := title + FILESEXT
	data, err := os.ReadFile(PAGESDIR + filename)
	if err != nil {
		return nil, err
	}

	var page Page
	err = json.Unmarshal(data, &page)
	if err != nil {
		return nil, err
	}

	return &page, nil
}

type SecurityLevel int

const (
	High SecurityLevel = iota
	Medium
	Low
)

type User struct {
	Name     string        `json:"name"`
	Password string        `json:"password"`
	Level    SecurityLevel `json:"level"`
	Pages    []string      `json:"pages"`
}

func (u *User) save() error {
	filename := u.Name + FILESEXT
	data, err := json.Marshal(u)
	if err != nil {
		return err
	}
	return os.WriteFile(USERSDIR+filename, data, 0600)
}

func loadUser(name string) (*User, error) {
	filename := name + FILESEXT
	data, err := os.ReadFile(USERSDIR + filename)
	if err != nil {
		return nil, err
	}

	var user User
	err = json.Unmarshal(data, &user)
	if err != nil {
		return nil, err
	}

	return &user, nil
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	body, err := os.ReadFile("index.html")
	if err != nil {
		http.NotFound(w, r)
	}
	fmt.Fprintf(w, "%s", body)
}

func viewHandler(w http.ResponseWriter, r *http.Request, title string) {
	p, err := loadPage(title)
	if err != nil {
		http.Redirect(w, r, "/edit/"+title, http.StatusFound)
		return
	}
	renderTemplate(w, "view", p)
}

func userHandler(w http.ResponseWriter, r *http.Request, name string) {
	u, err := loadUser(name)
	if err != nil {
		http.NotFound(w, r)
		return
	}
	renderTemplate(w, "user", u)
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	name := r.FormValue("username")
	pass := r.FormValue("password")

	user, err := loadUser(name)

	if err != nil {
		http.Error(w, "Bad Request", 400)
		return
	}

	if user.Password == "" || user.Password != pass {
		http.Error(w, "Bad Request", 400)
		return
	}

	session, err := encrypt(name)

	if err != nil {
		http.Error(w, "Bad Request", 400)
		return
	}

	cookie := http.Cookie{
		Name:     "session",
		Value:    session,
		MaxAge:   0,
		Secure:   false,
		HttpOnly: false,
		SameSite: http.SameSiteNoneMode,
	}
	http.SetCookie(w, &cookie)

	http.Redirect(w, r, "/user/"+name, http.StatusFound)
}

func editHandler(w http.ResponseWriter, r *http.Request, title string) {
	p, err := loadPage(title)
	if err != nil {
		p = &Page{Title: title}
	}
	renderTemplate(w, "edit", p)
}

func saveHandler(w http.ResponseWriter, r *http.Request, title string) {
	body := r.FormValue("body")
	private := r.FormValue("private")
	p := &Page{Title: title, Body: template.HTML(body), Private: private != ""}
	err := p.save()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	http.Redirect(w, r, "/view/"+title, http.StatusFound)
}

var templates = template.Must(template.ParseFiles("edit.html", "view.html", "user.html"))

func renderTemplate(w http.ResponseWriter, tmpl string, data any) {
	err := templates.ExecuteTemplate(w, tmpl+".html", data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

var secretKey = "d58f74a90cfd53dc17c4ebc43fb52a0d"

func encrypt(plaintext string) (string, error) {
	aes, err := aes.NewCipher([]byte(secretKey))
	if err != nil {
		return "", errors.New("AES failed")
	}

	gcm, err := cipher.NewGCM(aes)
	if err != nil {
		return "", errors.New("GCM failed")
	}

	// We need a 12-byte nonce for GCM (modifiable if you use cipher.NewGCMWithNonceSize())
	// A nonce should always be randomly generated for every encryption.
	nonce := make([]byte, gcm.NonceSize())
	_, err = rand.Read(nonce)
	if err != nil {
		return "", errors.New("Nonce failed")
	}
	// ciphertext here is actually nonce+ciphertext
	// So that when we decrypt, just knowing the nonce size
	// is enough to separate it from the ciphertext.
	ciphertext := gcm.Seal(nonce, nonce, []byte(plaintext), nil)

	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

func decrypt(ciphertext string) (string, error) {
	aes, err := aes.NewCipher([]byte(secretKey))
	if err != nil {
		return "", errors.New("AES failed")
	}

	gcm, err := cipher.NewGCM(aes)
	if err != nil {
		return "", errors.New("GCM failed")
	}

	bciphertext, err := base64.StdEncoding.DecodeString(ciphertext)
	if err != nil {
		return "", errors.New("Base64 failed")
	}
	ciphertext = string(bciphertext)

	// Since we know the ciphertext is actually nonce+ciphertext
	// And len(nonce) == NonceSize(). We can separate the two.
	nonceSize := gcm.NonceSize()

	if len(ciphertext) <= nonceSize {
		return "", errors.New("ciphertext invalid")
	}

	nonce, ciphertext := ciphertext[:nonceSize], ciphertext[nonceSize:]

	plaintext, err := gcm.Open(nil, []byte(nonce), []byte(ciphertext), nil)
	if err != nil {
		return "", errors.New("GCM decrypt failed")
	}

	return string(plaintext), nil
}

func contains(pages []string, page string) bool {
	for _, pn := range pages {
		if pn == page {
			return true
		}
	}
	return false
}

func validateSession(session *http.Cookie, url []string) (error, int) {
	username, err := decrypt(session.Value)
	if err != nil {
		return errors.New("Unauthorized"), 401
	}

	user, err := loadUser(username)

	if err != nil {
		return errors.New("Unauthorized"), 401
	}

	authorized := false

	if url[1] == "user" {
		if user.Name != url[2] {
			viewUser, err := loadUser(url[2])
			if err == nil && user.Level < viewUser.Level {
				authorized = true
			}
		} else {
			authorized = true
		}
	} else if url[1] == "view" {
		if user.Level == High || contains(user.Pages, url[2]) {
			authorized = true
		} else {
			page, err := loadPage(url[2])
			if err == nil && !page.Private {
				authorized = true
			}
		}
	} else if url[1] == "edit" || url[1] == "save" {
		if contains(user.Pages, url[2]) {
			authorized = true
		}
	}

	if !authorized {
		return errors.New("Forbidden"), 403
	}

	return nil, 0
}

var validPath = regexp.MustCompile("^/(edit|save|view|user)/([a-zA-Z0-9 ]+)$")

func makeHandler(fn func(http.ResponseWriter, *http.Request, string)) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		m := validPath.FindStringSubmatch(r.URL.Path)
		if m == nil {
			http.NotFound(w, r)
			return
		}

		session, err := r.Cookie("session")
		if err != nil {
			http.Error(w, "Unauthorized", 401)
			return
		}

		err, code := validateSession(session, m)
		if err != nil {
			http.Error(w, err.Error(), code)
			return
		}

		fn(w, r, m[2])
	}
}

func main() {
	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/view/", makeHandler(viewHandler))
	http.HandleFunc("/user/", makeHandler(userHandler))
	http.HandleFunc("/edit/", makeHandler(editHandler))
	http.HandleFunc("/save/", makeHandler(saveHandler))

	log.Fatal(http.ListenAndServe(":8080", nil))
}
