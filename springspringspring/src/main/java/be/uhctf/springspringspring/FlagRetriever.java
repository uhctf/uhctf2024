package be.uhctf.springspringspring;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import org.json.JSONObject;

public class FlagRetriever {
    public static String getFlag(String code) {
        try {

            URL url = new URL("https://ctf.wardsegers.be/spring.php?code=" + code);
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer content = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();
            String response = content.toString();
            JSONObject res_json = new JSONObject(response);
            String flag = res_json.getString("🏳️");
            return flag;
        } catch (Exception e) {
            System.err.println(e);
            return "EXCEPTION (possible network error)";
        }
    }
}
