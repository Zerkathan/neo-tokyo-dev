#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Web scraper legacy - Python 2.7 (circa 2012)
# Autor: Desconocido
# Última modificación: 2012-03-15
# TODO: Reescribir esto algún día...

import urllib2
import re
import time
import sys

# Variables globales (mala práctica)
BASE_URL = "http://example.com"
USER_AGENT = "MyBot/1.0"
DELAY = 0  # Sin delays = ban seguro

def get_page(url):
    """Get webpage content (sin manejo de errores)"""
    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    response = urllib2.urlopen(req)  # Sin timeout, sin try/except
    html = response.read()
    return html

def extract_links(html):
    """Extract links usando regex (muy frágil)"""
    # Regex horrible que rompe con HTML mal formado
    pattern = r'<a\s+href=["\']([^"\']+)["\']'
    links = re.findall(pattern, html)
    return links

def extract_emails(html):
    """Extract emails con regex simple"""
    # Regex simplista que matchea cosas que no son emails
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(pattern, html)
    return emails

def extract_prices(html):
    """Extract precios (asume formato específico)"""
    # Solo funciona con $XX.XX, falla con otros formatos
    pattern = r'\$(\d+\.\d{2})'
    prices = re.findall(pattern, html)
    return [float(p) for p in prices]

def save_to_file(data, filename):
    """Guarda datos (sin encoding, sin manejo de errores)"""
    f = open(filename, 'w')  # Sin context manager
    for item in data:
        f.write(str(item) + '\n')
    f.close()  # Si hay error, el archivo queda abierto

def scrape_website(start_url, max_pages=10):
    """Función principal (todo mezclado)"""
    print "Starting scraper..."
    
    visited = []  # Lista (búsqueda O(n))
    to_visit = [start_url]
    
    all_emails = []
    all_prices = []
    page_count = 0
    
    while to_visit and page_count < max_pages:
        url = to_visit.pop(0)
        
        # Verificar si ya visitamos (O(n) lookup)
        if url in visited:
            continue
        
        print "Scraping: " + url
        
        # Get page (sin manejo de errores)
        html = get_page(url)
        visited.append(url)
        page_count += 1
        
        # Extract todo (sin validación)
        links = extract_links(html)
        emails = extract_emails(html)
        prices = extract_prices(html)
        
        # Agregar a listas globales (sin deduplicación)
        all_emails.extend(emails)
        all_prices.extend(prices)
        
        # Agregar links para visitar (sin filtrar externos)
        for link in links:
            if link.startswith('http'):
                to_visit.append(link)
            elif link.startswith('/'):
                to_visit.append(BASE_URL + link)
        
        # Sin delay = ban rápido
        # time.sleep(1) # Comentado porque "va muy lento"
    
    print "Scraping complete!"
    print "Pages visited: " + str(page_count)
    print "Emails found: " + str(len(all_emails))
    print "Prices found: " + str(len(all_prices))
    
    # Guardar sin manejo de errores
    save_to_file(all_emails, 'emails.txt')
    save_to_file(all_prices, 'prices.txt')
    
    return all_emails, all_prices

# Ejecución sin argumentos parseados
if __name__ == "__main__":
    # Hardcoded URL (no configurable)
    start_url = "http://example.com/productos"
    
    # Sin try/except = crash fácil
    emails, prices = scrape_website(start_url, max_pages=50)
    
    # Calcular promedio (sin verificar lista vacía)
    avg_price = sum(prices) / len(prices)  # Division by zero si prices vacío
    print "Average price: $" + str(avg_price)

# PROBLEMAS DEL CÓDIGO:
# 1. Python 2.7 (deprecated desde 2020)
# 2. urllib2 (reemplazado por requests)
# 3. Sin manejo de errores
# 4. Regex frágiles para HTML
# 5. Sin respetar robots.txt
# 6. Sin rate limiting
# 7. Sin async (bloqueante)
# 8. Lista para visited (O(n) lookup)
# 9. Sin deduplicación
# 10. Sin logging
# 11. Sin configuración externa
# 12. Memory leaks con archivos
# 13. Encoding issues
# 14. Sin user agent rotation
# 15. Sin proxy support

