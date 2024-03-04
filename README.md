# MEGAPLAN-API PROJECT

This project receives WhatsApp messages and forwards them to the client entity in Megaplan.

## Table of Contents
- Setup
- Usage
- Running the Project
- Testing

## Setup
1. Install Python.
2. Install Flask by running `pip install flask` in your terminal.

## Usage
The main functionality of this project is to receive WhatsApp messages and forward them to the client entity in Megaplan.

## Running the Project
1. If you already have it, insert megaplan access token into `config.env`.
2. Insert your Megaplan link into `config.env`.
3. Host port 8080.
4. Set up Touch-API webhooks so that they come to `/webhook`.
5. Run `main.py`.

## Testing
You can either use Touch-API webhooks or manually write requests. For example:
```bash
curl -X POST \ 
-H "Content-Type: application/json" \
-d '{"from":"+77777777777","to":"+7777777777","text":"someText"}' http://localhost:8080/webhook