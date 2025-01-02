# kraftbase

**# FastAPI Application 

This guide explains how to set up and run a FastAPI application using Docker, along with managing database migrations using Alembic.

---

## **Setup Instructions**

### **1. Clone the Repository**

Clone the repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>
```

### **2. Configure Environment Variables**

Copy the example `.env.example` file to `.env` and configure it with your database connection URL:

```bash
cp .env.example .env
```

Edit the `.env` file and replace `DATABASE_URL` with your database connection string.

---

## **Docker Commands**

### **1. Build Docker Images**

```bash
docker-compose build
```

### **2. Start Containers**

```bash
docker-compose up -d
```

### **3. Stop Containers**

```bash
docker-compose down
```

---

## **Alembic Commands**

Alembic is used for database migrations. Below are the steps to use Alembic inside the web container:

### **1. Access the Web Container**

Use the following command to open a Bash shell inside the running web container:

```bash
docker exec -it <container_name> bash
```

Replace `<container_name>` with the name of your web container. You can find the container name using:

```bash
docker ps
```


### **2. Run Alembic Commands**

Now, you can run the required Alembic commands. For example:

- **Initialize Alembic** (if not done already):

  ```bash
  alembic init alembic
  ```

- **Generate a New Migration**:

  ```bash
  alembic revision --autogenerate -m "Your migration message"
  ```

- **Apply Migrations (Upgrade)**:

  ```bash
  alembic upgrade head
  ```

- **Rollback Migrations (Downgrade)**:

  ```bash
  alembic downgrade -1
  ```

- **Check Current Migration Version**:

  ```bash
  alembic current
  ```

### **3. Exit the Container**

After completing the migrations, you can exit the container by running:

```bash
exit
```
