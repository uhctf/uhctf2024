package be.uhctf.springspringspring;

import org.springframework.context.annotation.Configuration;
import org.springframework.shell.command.annotation.Command;
import org.springframework.shell.standard.ShellComponent;
import org.springframework.shell.standard.ShellMethod;
import org.springframework.shell.standard.ShellOption;
import org.springframework.stereotype.Component;

@ShellComponent
public class CodeChecker {
    private static final String CORRECT_PIN_SHA512 = "69edd447655e95cf4ad0e987e14e0c97d8aca399a8681d8be1062bbb8030515ce48ba58b8da4e02164785a947b4e4fa0f946185f05d4f18150d0cd76452ea60c";

    @ShellMethod("checks if your Spring pincode is good and will retrieve a flag if it is.")
    public static String validatePincode(String pincode) {
        if (pincode == null)
            return "pincode is null";

        String pc = pincode;
        if (pc.length() != 9) {
            return "The pincode \"" + pc + "\" must contain exactly 9 digits (now containging " + pc.length() + ")";
        }
        String hashed = SHA512sum.calculateSHA512(pc);
        if (!hashed.equals(CORRECT_PIN_SHA512))
            return "This pincode is not correct";

        System.out.println("This pincode is correct! Fetching flag…");
        return FlagRetriever.getFlag(pc);
    }
}
