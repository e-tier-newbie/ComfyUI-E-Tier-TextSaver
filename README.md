# E_TierTextSaver
For everyone who's sick of <pad>😂

This is a custom ComfyUI node that saves processed text to a `.txt` file. The node allows you to remove any specified string from the input text (e.g., `<pad>`) and saves the cleaned result to disk using the provided image filename (with the extension removed).

## Features

- Removes any specified substring from the input text
- Automatically strips file extensions like `.png`, `.jpg`, `.webp`, etc.
- Saves the result as `.txt` file in a custom output directory
- Lightweight and easy to use

## Input Fields

| Field            | Description                                              |
|------------------|--------------------------------------------------|
| `text`              | The input string to clean and save            |
| `text_to_remove` | Substring to remove from the input        |
| `filename`       | Source filename (e.g., `image.png`)            |
| `output_dir`     | Directory to save the cleaned `.txt` file       |

## Installation

You can install this node manually by placing it in your `custom_nodes` folder or clone via ComfyUI Manager using:

