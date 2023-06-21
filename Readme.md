<h1>Search Engine GUI using Duck Duck Go</h1>

<h2>Installation</h2>

```bash
pip install -r requirements.txt

```

<h3>Note : This search engine only supports DuckDuckGo search at this time</h3>

<h2>Dependencies</h2>

<p>This project relies on following libraries: </p>

```python
import tkinter as tk
import webbrowser
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import tkinter.ttk as ttk


```

<h2>To Make the Code Executable</h3>


```bash
cd pyinstaller-4.7
```
<p> Then write this command: </p>

```bash
python pyinstaller --onefile ..\searchengine.py --windowed
```

<p>And The Executable file is in dist directory</p>

```bash
cd dist\searchengine.exe
```
<h3>Note that if you have problem with this pyinstaller package, you can uninstall it and install the new one</h3>

<p>Uinstall the pyinstaller using command: </p>

```python
pip uninstall pyinstaller

```

<p>Install the pyinstaller using command: </p>

```python
pip install pyinstaller

```