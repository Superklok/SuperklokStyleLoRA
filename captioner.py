import os

# Path to your exact style dataset folder
dataset_folder = os.path.join("dataset", "20_SuperklokStyle")
trigger_word = "Superklok Style"

# This description isolates the text so the letters don't permanently bake into your style
text_protection_caption = (
    "The graphic features text overlay that reads 'Superklok Labs'. "
    "The lettering is rendered in a sharp, glowing color retro-terminal font with a bold black shadow outline."
)

if not os.path.exists(dataset_folder):
    print(f"Error: The directory '{dataset_folder}' does not exist. Please check your folder path.")
else:
    count = 0
    # Loop over all files in the directory
    for filename in os.listdir(dataset_folder):
        if filename.lower().endswith('.png'):
            # Strip the extension
            base_name = filename[:-4]
            txt_filename = f"{base_name}.txt"
            txt_path = os.path.join(dataset_folder, txt_filename)
            
            # Combine your new brand trigger word and the text protection caption
            full_style_caption = f"{trigger_word}, {text_protection_caption}"
            
            # Write a fresh text file with the updated layout
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(full_style_caption)
            count += 1

    print(f"Success! Re-generated {count} text files using your brand trigger: '{trigger_word}'.")
