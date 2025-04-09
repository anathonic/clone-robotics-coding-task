# [Coding Task] Full Stack Developer

Hello to the entire Clone Robotics team!

Everything is set up fine if we run the application through Docker. However, when changing the backend port, we need to update it in the following places:

1. **Commands**: Ensure that the backend service is started with the correct port.
2. **Port Mapping**: Update the port mapping in the `docker-compose.yml` file.
3. **Frontend Environment Variable**: Update the `VITE_API_URL` in the frontend's Docker configuration to match the new backend port.

### CORS Configuration
CORS in the backend is set to allow all URLs, so the frontend port can be safely changed in Docker without any issues.
