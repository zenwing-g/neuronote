# **NeuroNote**

## **Description**

NeuroNote is an **innovative note-taking app** that structures information as a **network of interconnected notes**, rather than traditional linear documents.

### **How It Works**

- You create a **book** (a folder) to organize related notes.
- Each note, called a **page**, is stored as a file inside the book.
- Pages contain **content** and **links to other pages**, forming a **dynamic knowledge network**.
- The app provides a **graph-based GUI**, allowing you to **visually explore and navigate** connections between notes.

This approach helps in **structuring knowledge**, making it easier to **connect ideas, recall information, and visualize relationships**. 🚀

---

## **Technologies Used**

### **🖥️ Frontend (User Interface)**

- **PyQt6** → For building the desktop GUI
- **PyQtGraph** → For rendering the interactive network of notes
- **Markdown2** → For displaying and formatting text content
- **MathJax** → For rendering LaTeX equations inside notes

### **📂 Backend (Data Storage & Management)**

- **File-Based Storage** → Notes are stored as files inside structured folders
- **CSV Files (`ids.csv`, `links.csv`)** → For managing note connections
- **Python’s `os` & `pathlib`** → For file management

### **🔗 Graph Structure & Linking**

- **NetworkX** → For handling the relationships between notes
- **PyQtGraph** → For rendering the network visualization

---

> **NeuroNote is an offline-first, lightweight, and highly visual note-taking app that makes organizing and connecting ideas effortless. With a structured folder-based system, interactive graph visualization, and seamless Markdown support, it offers a unique way to manage and explore information.**

---

### How to use

- Opening the app greets you with the welcome screen which contains the logo a search bar and the open button.
- Click on the search bar and a drop down menu appears with the list of books.
- Select the required book and click on the open button.
- This opens the selected book in the graph view where you can visualize your notes in the form of neural network.
- Double click on the graph to create a new page. Things are set on auto-save.
- Click and drag the sides of a page to form a link between the desired pages.
- Left clicking on a page, link or the graph will give the respective functions available.
