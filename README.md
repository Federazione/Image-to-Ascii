<div align="center">
  <img src="https://raw.githubusercontent.com/Federazione/Image-to-Ascii/main/assets/banner.png" alt="Image to ASCII Banner" width="900">
  <h1>Image to ASCII</h1>
  <p><strong>Transform images into stunning ASCII art in seconds.</strong></p>
  <p>
    <a href="#">
      <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
    </a>
  </p>
</div>

<div align="center">
  <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80" alt="Project preview" width="900">
</div>

<h2>✨ Overview</h2>

<p>
  <strong>Image to ASCII</strong> is a lightweight tool that converts an image into an ASCII-style representation while preserving the visual essence of the original.
  It is perfect for creative coding projects, terminal-based visualizations, retro aesthetics, and quick artistic experiments.
</p>

<p>
  Whether you want to generate artistic text from a photo, create a terminal-based display, or simply explore a fun way to transform images, this project gives you an elegant and easy-to-use solution.
</p>

<hr />

<h2>🚀 Features</h2>

<ul>
  <li>Convert images to ASCII art with customizable density and contrast.</li>
  <li>Supports multiple image formats.</li>
  <li>Simple command-line usage.</li>
  <li>Fast rendering with clean output.</li>
  <li>Flexible configuration for width, height, and character set.</li>
</ul>

<hr />

<h2>🛠️ Installation</h2>

```bash
git clone https://github.com/Federazione/Image-to-Ascii.git
cd Image-to-Ascii
pip install -r requirements.txt
```

<hr />

<h2>📌 Usage</h2>

```bash
python main.py input.jpg --width 120 --contrast 1.5
```

You can also try:

```bash
python main.py image.png --width 80 --chars " .:-=+*#%@"
```

<h3>Available options</h3>

```bash
--input        Path to the source image
--width        Width of the ASCII output
--height       Optional custom height
--chars        Character set used for rendering
--contrast     Adjust contrast for sharper results
--invert       Invert the ASCII output
```

<hr />

<h2>🎨 Example</h2>

<p>Original image:</p>

<img src="https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=900&q=80" alt="Sample image" width="500">

<p>ASCII output:</p>

```text
                 .,:;irsXA253hSAMl30
             .,:;irsXA253hSAl30
         .,:;irsXA253hSAm3
       .,:;irsXA253hSAl
      .,:;irsXA253hSAl
        .,;irsXA253hSAl
           .,;irsXA253hSAl
             .,:;irsXA253hSAlc
                 .,:;irsXA253hSAl
                    .,:;irsXA253hS
```

<hr />

<h2>📁 Project Structure</h2>

```text
Image-to-Ascii/
├── main.py
├── README.md
├── requirements.txt
├── assets/
│   └── banner.png
├── src/
│   ├── converter.py
│   └── utils.py
└── examples/
    └── sample.jpg
```

<hr />

<h2>🤝 Contributing</h2>

<p>
  Contributions are welcome! If you’d like to improve the project, feel free to open an issue or submit a pull request.
</p>

```bash
git checkout -b feature/my-improvement
git commit -m "Add a new ASCII rendering option"
git push origin feature/my-improvement
```

<hr />

<h2>📜 License</h2>

<p>
  This project is licensed under the <a href="#">MIT License</a>.
</p>

<div align="center">
  <p><strong>Made with ❤️ for creative coding and retro-style visuals.</strong></p>
</div>
