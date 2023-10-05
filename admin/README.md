# Админка

## Локализация

Из директории `admin`:

- Извлечь переводимые строки из заданных входных файлов.

```
xgettext -j --language=Python --keyword=_ --output=locales/ru/LC_MESSAGES/base.po models.py
```

Опция `-j` дописывать существующий файл


- Скомпилировать перевод

```
msgfmt locales/ru/LC_MESSAGES/base.po -o locales/ru/LC_MESSAGES/base.mo
```

