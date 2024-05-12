import random
import sys
from uhctf import print_flag
import yaml

# PyYAML 3.13 compatibility fix
import collections.abc
collections.Hashable = collections.abc.Hashable

def load_configuration(config_file):
    try:
        with open(config_file, "rb") as file:
            data = file.read()
            config = yaml.load(data)
            return config
    except FileNotFoundError:
        print("Error: Configuration file not found.")
    except yaml.YAMLError as e:
        print(f"Error: YAML parsing error: {e}")
    return None

def generate_parseltongue_text(config):
    if config:
        try:
            generator_config = config.get("parseltongue_generator_config", {})
            settings = generator_config.get("settings", {})
            snake_sounds = settings.get("snake_sounds", [])
            length = settings.get("length", 100)
            vowels = settings.get("vowels", "aeiou")
            consonants = settings.get("consonants", "sltrngy")
            allow_repetition = settings.get("repetition", True)
        except:
            return "Error: Unable to parse generator configuration"


        generated_text = ""
        for _ in range(length):
            if allow_repetition:
                sound = snake_sounds[random.randint(0, len(snake_sounds) - 1)]
            else:
                available_sounds = [s for s in snake_sounds if s != generated_text[-len(s):]]
                if available_sounds:
                    sound = random.choice(available_sounds)
                else:
                    sound = random.choice(snake_sounds)
            generated_text += random.choice(consonants) + sound + random.choice(vowels)

        return "Generated Parseltongue Text:\n" + generated_text

    return "Error: Unable to generate Parseltongue text due to missing configuration."

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_file_path>")
        return
    
    config_file = sys.argv[1]
    config = load_configuration(config_file)

    parseltongue_text = generate_parseltongue_text(config)
    print(parseltongue_text)

if __name__ == "__main__":
    main()
