# Restaurant Menu Automation Service

## Overview

This project provides an automation service that retrieves the menu for your favorite restaurants using web scraping (with Selenium) and OCR techniques (with Tesseract). The service is built using FastAPI for the API layer, and the data is stored in a MongoDB database.

## Features

- **FastAPI**: Provides a RESTful API to interact with the service.
- **MongoDB**: Stores the restaurant menus for quick retrieval.
- **Web Scraping with Selenium**: Utilizes Selenium for browser automation to scrape menus from restaurant websites.
- **OCR with Tesseract**: Employs Tesseract for optical character recognition to extract text from images of menus.
- **Pydantic**: Ensures data validation and serialization.

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB
- Tesseract-OCR
- Selenium WebDriver

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Atharv-a/menu_data_extractor_automation.git
   cd restaurant-menu-automation
