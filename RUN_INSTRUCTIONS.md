# Step-by-Step: How to Run the Docker Setup

## Prerequisites Check ✅

Make sure Docker is installed:
```bash
docker --version
docker-compose --version
```

If not installed, download from: https://www.docker.com/products/docker-desktop

---

## Step 1: Navigate to Project Directory

```bash
cd /Users/elakia/Documents/CODE/sample/communal_collage_activity
```

Or if you're already in the project folder, verify you're in the right place:
```bash
pwd
ls -la
```

You should see:
- `Dockerfile`
- `docker-compose.yml`
- `app.py`
- `requirements.txt`
- `config.py`

---

## Step 2: Check Port Availability

Make sure ports 5001, 9000, and 9001 are not in use:

```bash
# Check if ports are available
lsof -i :5001
lsof -i :9000
lsof -i :9001
```

If any port is in use, you'll need to stop that service first or change the ports in `docker-compose.yml`.

---

## Step 3: Build and Start Services

### Option A: Using Docker Compose (Recommended)

```bash
# Build images and start containers in detached mode
docker-compose up -d --build
```

**What this does:**
- `up` - Starts the containers
- `-d` - Runs in detached mode (background)
- `--build` - Builds the Docker image from Dockerfile before starting

### Option B: Using the Convenience Script

```bash
# Make sure script is executable
chmod +x docker-run.sh

# Run the script
./docker-run.sh
```

---

## Step 4: Verify Services Are Running

Check the status of your containers:

```bash
docker-compose ps
```

You should see both services running:
```
NAME                          STATUS
communal-collage-activity-app-1    Up
communal-collage-activity-minio-1  Up
```

Or check with Docker directly:
```bash
docker ps
```

---

## Step 5: View Logs (Optional but Recommended)

To see what's happening:

```bash
# View all logs
docker-compose logs -f

# View only Flask app logs
docker-compose logs -f app

# View only MinIO logs
docker-compose logs -f minio
```

Press `Ctrl+C` to exit log viewing.

---

## Step 6: Access Your Application

Once containers are running, open your browser:

### Flask Application
- **URL**: http://localhost:5001
- This is your main application where you can upload images

### MinIO Admin Console
- **URL**: http://localhost:9001
- **Username**: `admin`
- **Password**: `password123`
- This is for managing object storage

---

## Step 7: Test the Application

1. Open http://localhost:5001 in your browser
2. Click "Get Daily Token" to generate a token
3. Select an image file
4. Click "Upload to Collage"
5. Your image should upload successfully!

---

## Common Commands

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

### View Container Status
```bash
docker-compose ps
```

### Stop and Remove Everything (including volumes)
```bash
docker-compose down -v
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find what's using the port
lsof -i :5001

# Stop the containers
docker-compose down

# Change ports in docker-compose.yml if needed
```

### Containers Won't Start
```bash
# Check logs for errors
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Can't Access Application
1. Check if containers are running: `docker-compose ps`
2. Check logs: `docker-compose logs app`
3. Verify ports: `docker ps` (check PORT column)
4. Try accessing http://127.0.0.1:5001 instead of localhost

### Need to See What's Inside Container
```bash
# Access Flask app container shell
docker-compose exec app bash

# Access MinIO container shell
docker-compose exec minio sh
```

---

## Complete Example Session

```bash
# 1. Navigate to project
cd /Users/elakia/Documents/CODE/sample/communal_collage_activity

# 2. Start everything
docker-compose up -d --build

# 3. Check status
docker-compose ps

# 4. View logs (optional)
docker-compose logs -f app

# 5. Open browser to http://localhost:5001

# 6. When done, stop everything
docker-compose down
```

---

## What Gets Started?

1. **MinIO Container** (minio/minio image)
   - Object storage server
   - Ports: 9000 (API), 9001 (Admin UI)
   - Data stored in: `./minio_data` folder

2. **Flask App Container** (built from Dockerfile)
   - Your Flask application
   - Port: 5001
   - Connected to MinIO via Docker network
   - Data stored in: `./temp_uploads` and `./local_storage` folders

Both run in **detached mode** (background) and auto-restart if they crash.

