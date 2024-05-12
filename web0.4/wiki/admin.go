package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"errors"
)

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

func main() {
	cookie, err := encrypt("admin")
	if err != nil {
		panic(err)
	}
	println(cookie)
}
