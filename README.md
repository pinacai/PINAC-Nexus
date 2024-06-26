<div align="center">

<h1 style="border-bottom: none">
    <b><a href="https://github.com/pinacai">PINAC-Nexus</a></b><br>
    Uplifting the AI Generated Text Quality
</h1>

<img src="https://github.com/pinacai/PINAC-Nexus/blob/main/assets/header.png" alt="header image">

<br>
<br>

![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
[![View Repositories](https://img.shields.io/badge/View-Our_Repositories-blue?logo=GitHub)](https://github.com/pinacai?tab=repositories)

A simple to use framework for getting high quality text for different task using AI.  
Inspired by <a href="https://github.com/danielmiessler/fabric">Fabric</a>. Taking it to the next level !

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

</div>

## Why PINAC-Nexus ?
May be you are like me, not a prompt engineer, neither like to write long prompt for a simple task but still we deserve the best result. So, I made this console tool so that you can tell your need in short and simple words and this tool will generate the best result for you!

Inspired by <a href="https://github.com/danielmiessler/fabric">Fabric</a> but making it even better, removing the need of remembering particular command, making simple to use.

If you want a cool Desktop app with this tool, visit our App <a href="https://github.com/pinacai/PINAC_Workspace">**PINAC Workspace**</a>. I am sure it will make you day.


## System Design

<img src="https://github.com/pinacai/PINAC-Nexus/blob/main/assets/system%20design.svg" alt="System Design Diagram">


##  🚀 Project Setup
Follow these few steps to set up the server for **PINAC Workspace** on your system:

### Prerequisites
- _Python_
- _OPENAI API Key_ & _GEMINI API KEY_
    > **NOTE**: If you have only either OPENAI or GEMINI KEY, then you just need to do some change in `main.py` and it's easy.
- _Internet Connection_

1. Clone the Repository
    ```bash
    git clone https://github.com/pinacai/PINAC-Nexus.git && cd "PINAC-Nexus"
    ```

2. Create virtualenv & activate it
    ```bash
    python -m venv env && source env/bin/activate
    ```

3. Install python dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Now get your API Keys and to place it create `.env` file in the folder `configs/` and copy-paste the below line in `.env`:
    ```
    OPENAI_API_KEY = "<Place your OPENAI API Key here>"

    GOOGLE_API_KEY = "<Place your GEMINI API Key here>"
    ```

5. Run the `main.py` file.
