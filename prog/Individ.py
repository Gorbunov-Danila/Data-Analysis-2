#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
import os

def create_sample_input_file(file_path):
    """
    Создает файл с примерным содержимым, если файл не существует.
    """
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                sample_text = ("Это первое предложение. Второе предложение, с запятой. Третье предложение без запятой!")
                file.write(sample_text)
            print(f"Файл '{file_path}' создан с примерным содержимым.")
        else:
            print(f"Файл '{file_path}' уже существует.")
    except Exception as e:
        print(f"Ошибка при создании файла '{file_path}': {e}")

def read_file(file_path):
    """
    Считывает текст из файла и возвращает его содержимое.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"Содержимое файла '{file_path}':\n{content}")
            return content
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла '{file_path}': {e}")
        return None

def split_into_sentences(text):
    """
    Разделяет текст на предложения.
    """
    try:
        sentence_endings = re.compile(r'[.!?]')
        sentences = sentence_endings.split(text)
        print(f"Разделенные предложения: {sentences}")
        return [sentence.strip() for sentence in sentences if sentence.strip()]
    except Exception as e:
        print(f"Ошибка при разделении текста на предложения: {e}")
        return []

def filter_sentences(sentences):
    """
    Возвращает список предложений, не содержащих запятых.
    """
    try:
        filtered = [sentence for sentence in sentences if ',' not in sentence]
        print(f"Отфильтрованные предложения (без запятых): {filtered}")
        return filtered
    except Exception as e:
        print(f"Ошибка при фильтрации предложений: {e}")
        return []

def save_to_json(data, file_path):
    """
    Сохраняет данные в файл формата JSON.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в файл '{file_path}'")
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл '{file_path}': {e}")

def load_from_json(file_path):
    """
    Загружает данные из файла формата JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Загруженные данные из '{file_path}': {data}")
            return data
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке данных из файла '{file_path}': {e}")
        return None

def main():
    """
    Главная функция программы.
    """
    # Указываем пути к файлам
    input_file_path = 'input.txt'
    json_file_path = 'filtered_sentences.json'

    # Создаем файл с примерным содержимым, если он не существует
    create_sample_input_file(input_file_path)

    # Считываем текст из файла
    text = read_file(input_file_path)
    if text is None:
        return  # Завершаем программу, если не удалось прочитать файл

    # Разделяем текст на предложения
    sentences = split_into_sentences(text)

    # Фильтруем предложения без запятых
    filtered_sentences = filter_sentences(sentences)
    
    # Сохраняем отфильтрованные предложения в JSON-файл
    save_to_json(filtered_sentences, json_file_path)
    
    # Загружаем отфильтрованные предложения из JSON-файла
    loaded_sentences = load_from_json(json_file_path)
    if loaded_sentences is None:
        return  # Завершаем программу, если не удалось загрузить файл
    
    print("Предложения без запятых:")
    for sentence in loaded_sentences:
        print(sentence)

if __name__ == "__main__":
    main()
