#!/usr/bin/env python
# Sistema de gestión de biblioteca - CÓDIGO LEGACY
# Este código "funciona" pero es una pesadilla mantenerlo

import json
import os
from datetime import datetime

def main():
    # Todo en una función gigante
    print("=== SISTEMA DE BIBLIOTECA ===")
    
    # Variables globales escondidas como locales
    books = []
    users = []
    loans = []
    
    # Cargar datos (mezclado con lógica)
    if os.path.exists("books.json"):
        with open("books.json") as f:
            books = json.load(f)
    if os.path.exists("users.json"):
        with open("users.json") as f:
            users = json.load(f)
    if os.path.exists("loans.json"):
        with open("loans.json") as f:
            loans = json.load(f)
    
    while True:
        print("\n1. Agregar libro")
        print("2. Registrar usuario")
        print("3. Prestar libro")
        print("4. Devolver libro")
        print("5. Ver libros disponibles")
        print("6. Ver préstamos activos")
        print("7. Salir")
        
        opt = input("Opción: ")
        
        if opt == "1":
            # Agregar libro (sin validación)
            t = input("Título: ")
            a = input("Autor: ")
            y = input("Año: ")
            isbn = input("ISBN: ")
            
            # ID generado de forma rara
            id = len(books) + 1
            
            # Append directo sin validar duplicados
            books.append({
                "id": id,
                "title": t,
                "author": a,
                "year": int(y),
                "isbn": isbn,
                "available": True
            })
            
            # Guardar inmediatamente (sin manejo de errores)
            with open("books.json", "w") as f:
                json.dump(books, f)
            
            print("Libro agregado!")
            
        elif opt == "2":
            # Registrar usuario (código duplicado del bloque anterior)
            n = input("Nombre: ")
            e = input("Email: ")
            
            id = len(users) + 1
            
            users.append({
                "id": id,
                "name": n,
                "email": e,
                "active": True
            })
            
            with open("users.json", "w") as f:
                json.dump(users, f)
            
            print("Usuario registrado!")
            
        elif opt == "3":
            # Prestar libro (lógica compleja sin separar)
            user_id = int(input("ID de usuario: "))
            book_id = int(input("ID de libro: "))
            
            # Buscar usuario (búsqueda ineficiente)
            u = None
            for user in users:
                if user["id"] == user_id:
                    u = user
                    break
            
            if u is None:
                print("Usuario no encontrado")
                continue
            
            if not u["active"]:
                print("Usuario inactivo")
                continue
            
            # Buscar libro (misma lógica duplicada)
            b = None
            for book in books:
                if book["id"] == book_id:
                    b = book
                    break
            
            if b is None:
                print("Libro no encontrado")
                continue
            
            if not b["available"]:
                print("Libro no disponible")
                continue
            
            # Verificar si usuario tiene préstamos vencidos (lógica anidada)
            has_overdue = False
            for loan in loans:
                if loan["user_id"] == user_id and loan["status"] == "active":
                    # Calcular días (lógica de fecha mezclada)
                    loan_date = datetime.strptime(loan["date"], "%Y-%m-%d")
                    days = (datetime.now() - loan_date).days
                    if days > 14:
                        has_overdue = True
                        break
            
            if has_overdue:
                print("Usuario tiene préstamos vencidos!")
                continue
            
            # Crear préstamo
            loan_id = len(loans) + 1
            loans.append({
                "id": loan_id,
                "user_id": user_id,
                "book_id": book_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "active"
            })
            
            # Actualizar disponibilidad del libro
            for i in range(len(books)):
                if books[i]["id"] == book_id:
                    books[i]["available"] = False
                    break
            
            # Guardar todo (sin transacciones, puede corromperse)
            with open("books.json", "w") as f:
                json.dump(books, f)
            with open("loans.json", "w") as f:
                json.dump(loans, f)
            
            print("Libro prestado!")
            
        elif opt == "4":
            # Devolver libro (más código duplicado)
            loan_id = int(input("ID de préstamo: "))
            
            l = None
            for loan in loans:
                if loan["id"] == loan_id:
                    l = loan
                    break
            
            if l is None:
                print("Préstamo no encontrado")
                continue
            
            if l["status"] != "active":
                print("Préstamo ya cerrado")
                continue
            
            # Calcular multa si está vencido
            loan_date = datetime.strptime(l["date"], "%Y-%m-%d")
            days = (datetime.now() - loan_date).days
            
            if days > 14:
                overdue_days = days - 14
                fine = overdue_days * 0.50  # $0.50 por día
                print(f"ATENCIÓN: Préstamo vencido. Multa: ${fine:.2f}")
            
            # Actualizar préstamo
            for i in range(len(loans)):
                if loans[i]["id"] == loan_id:
                    loans[i]["status"] = "returned"
                    loans[i]["return_date"] = datetime.now().strftime("%Y-%m-%d")
                    break
            
            # Actualizar libro
            book_id = l["book_id"]
            for i in range(len(books)):
                if books[i]["id"] == book_id:
                    books[i]["available"] = True
                    break
            
            with open("books.json", "w") as f:
                json.dump(books, f)
            with open("loans.json", "w") as f:
                json.dump(loans, f)
            
            print("Libro devuelto!")
            
        elif opt == "5":
            # Ver libros (sin paginación, sin ordenamiento)
            print("\n=== LIBROS DISPONIBLES ===")
            count = 0
            for book in books:
                if book["available"]:
                    print(f"{book['id']}. {book['title']} - {book['author']} ({book['year']})")
                    count += 1
            
            if count == 0:
                print("No hay libros disponibles")
                
        elif opt == "6":
            # Ver préstamos activos (join manual de datos)
            print("\n=== PRÉSTAMOS ACTIVOS ===")
            count = 0
            for loan in loans:
                if loan["status"] == "active":
                    # Buscar usuario
                    user_name = "?"
                    for user in users:
                        if user["id"] == loan["user_id"]:
                            user_name = user["name"]
                            break
                    
                    # Buscar libro
                    book_title = "?"
                    for book in books:
                        if book["id"] == loan["book_id"]:
                            book_title = book["title"]
                            break
                    
                    # Calcular días
                    loan_date = datetime.strptime(loan["date"], "%Y-%m-%d")
                    days = (datetime.now() - loan_date).days
                    
                    status = "OK" if days <= 14 else "VENCIDO"
                    
                    print(f"{loan['id']}. {user_name} - {book_title} ({days} días) [{status}]")
                    count += 1
            
            if count == 0:
                print("No hay préstamos activos")
                
        elif opt == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()

