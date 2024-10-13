## Page analyzer project
---

[![Actions Status](https://github.com/ross0maha/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ross0maha/python-project-83/actions)
[![Actions Status](https://github.com/ross0maha/python-project-83/actions/workflows/flake8.yml/badge.svg)](https://github.com/ross0maha/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/58419f74c40a6b65a5ce/maintainability)](https://codeclimate.com/github/ross0maha/python-project-83/maintainability)


## :link: [Demo on render.com](https://python-project-83-k000.onrender.com)

__*Анализатор страниц*__ представляет собой полноценное приложение, созданное на базе фреймворка **Flask**. Это приложение позволяет освоить и применить на практике основные принципы разработки современных сайтов, построенных на архитектуре **MVC**. В частности, в нём рассматриваются такие аспекты, как работа с роутингом, обработчиками запросов, шаблонизатором и взаимодействие с базой данных.

Анализатор страниц — это отличный инструмент для изучения основ веб-разработки с использованием Flask. Он помогает понять, как устроены современные сайты, и научиться создавать собственные веб-приложения. Данный проект является третьим проектом на курсе __*Python - разработчик*__ онлайн школы программирования **HEXLET**. 

_**Page Analyzer**_ is a full-fledged application based on the **Flask framework**. This application allows you to learn and apply in practice the basic principles of developing modern sites built on the _MVC architecture_. In particular, it covers such aspects as working with routing, request handlers, templating and database interaction.

The Page Analyzer is a great tool for learning the basics of web development using Flask. It helps you understand how modern websites are organized and learn how to build your own web applications. This project is the third project in the Python developer course of the online programming school _HEXLET_.

### :dizzy: Requirements
- Python 3.11
- Flask 3.0.3
- PostgreSQL 16

### :floppy_disk: Installation

Clone repository from github

```sh
clone git@github.com:ross0maha/python-project-83.git
```

```sh
pip instal poetry && pip install --update pip
```

```sh
make install
```

**Make migrations**

First you need to export the environment variable:

```sh
export DATABASE_URL = postgresql://user:password@database_host/database
```

and run
```sh
make migrate
```

### :muscle: Run server

```sh
make start
```

### :goberserk: Run flask server for local debuging

```sh
make dev
```
