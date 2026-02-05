@echo off
REM Run complete application (frontend + backend) with in-memory H2 database.
REM No MySQL, Redis, or Kafka required. Open http://localhost:8080 when started.
echo Starting Portfolio Manager (standalone)...
call mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=standalone
pause
