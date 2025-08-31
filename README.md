# 📸 Visual Product Matcher  

A web application that helps users find **visually similar products** based on uploaded images.  
Built as part of the **Software Engineering Technical Assessment Project**.  

---

## ✨ Features  

- 📤 **Image Upload**  
  - Upload images from local files or provide an image URL.  

- 🔍 **Search Interface**  
  - Displays the uploaded image.  
  - Shows a list of visually similar products.  
  - Supports filtering by similarity score.  

- 🗄️ **Product Database**  
  - MongoDB collection with 50+ products.  
  - Each product includes metadata: *name, category, image URL, and embedding vector*.  

- 📱 **Responsive Design**  
  - Frontend built with **HTML, CSS, JavaScript**.  
  - Optimized for both desktop and mobile.  

- 🌐 **Hosting & Deployment**  
  - **Frontend:** Netlify  
  - **Backend:** Render  
  - **Database:** MongoDB Atlas  

---

## 🛠️ Tech Stack  

- **Backend:** Python (FastAPI/Flask)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** MongoDB Atlas  
- **AI/ML:** Image embeddings for similarity search  
- **Deployment:** Netlify (frontend) & Render (backend)  

---

## 📂 Project Structure  

```bash
├── data/             # Product data
├── database/         # MongoDB connection & schema
├── frontend/         # Frontend files (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── models/           # ML models or embedding logic
├── routes/           # API routes (upload/search)
├── uploads/          # Uploaded images
├── utils/            # Helper functions
├── venv/             # Virtual environment
├── main.py           # Backend entry point
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (Mongo URI, keys, etc.)
└── README.md         # Documentation
````

---

## ⚙️ Installation & Setup

### 🔧 Backend (Python + MongoDB)

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/visual-product-matcher.git
   cd visual-product-matcher
   ```

2. **Create virtual environment & activate**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   Create a `.env` file in the project root:

   ```env
   MONGO_URI=your-mongodb-uri
   DB_NAME=your-db-name
   ```

5. **Run backend server locally**

   ```bash
   python main.py
   ```

---

### 🎨 Frontend (Netlify Deployment)

1. Navigate to the `frontend/` folder.
2. Deploy to **Netlify** (drag & drop OR connect GitHub repo).
3. Update API endpoints in `script.js` to point to your **Render backend URL**.

---

## 📖 Approach (200 Words)

The **Visual Product Matcher** solves the challenge of finding visually similar products by combining computer vision with a clean web interface. The backend, developed in Python, connects to a **MongoDB Atlas database** that stores product details and precomputed embeddings. When a user uploads an image or enters an image URL, embeddings are generated and compared with stored vectors using similarity scoring, returning the closest matches.

The frontend, hosted on Netlify, provides a responsive interface built with HTML, CSS, and JavaScript. It allows users to upload images, view their input, and see a list of recommended products with filtering options. The backend, deployed on Render, ensures scalability and quick API responses.

Error handling is integrated for invalid image links and missing data. Loading states enhance UX, while modular code structure ensures maintainability. With **MongoDB as the database** and **cloud hosting (Netlify + Render)**, the system is production-ready and reliable.

---

## ✅ Deliverables

* 🔗 **Live Application:** \[https://unthinkablevpm.netlify.app/]
* 💻 **GitHub Repository:** \[https://github.com/VanshSunejaa/unthinkable]

---



---

## 👨‍💻 Author

* **Vansh Suneja**
* GitHub: [@VanshSunejaa](https://github.com/VanshSunejaa)

---

```

---

