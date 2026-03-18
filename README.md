# Mini CRM Kommo – Multi-Tenant SaaS Architecture

## 🇺🇸 English

This project is a security-focused multi-tenant CRM built with Django and Django REST Framework.

### Architecture Highlights
- Column-based multi-tenancy (`organization_id`)
- Header-based tenant resolution (`X-Organization-ID`)
- Role-Based Access Control (RBAC)
- Strict tenant isolation (anti-IDOR protection)
- Pipeline & Stage module
- Pytest automated test suite
- Docker-ready environment

## 🧪 Tests & Quality

- Pytest with database isolation
- Multi-tenant validation
- RBAC (role-based access control)
- Pre-commit hooks (ruff, formatting, security checks)

## 🐳 Infrastructure

- PostgreSQL via Docker
- Environment-based settings (dev/test/prod)
- CI pipeline with GitHub Actions

---

## 🇧🇷 Português

Este projeto é um CRM multi-tenant com foco em segurança, desenvolvido com Django e Django REST Framework.

### Destaques da Arquitetura
- Multi-tenancy por coluna (`organization_id`)
- Resolução de organização via header (`X-Organization-ID`)
- Controle de acesso baseado em papéis (RBAC)
- Isolamento rigoroso entre organizações (proteção contra IDOR)
- Módulo de Pipeline e Stages
- Testes automatizados com Pytest
- Ambiente preparado para Docker

## 🧪 Testes e Qualidade

- Pytest com isolamento de banco de dados
- Validação multi-tenant
- RBAC (controle de acesso baseado em funções)
- Hooks de pré-commit (verificação de rascunho, formatação e segurança)

## 🐳 Infraestrutura

- PostgreSQL via Docker
- Configurações baseadas em ambiente (desenvolvimento/teste/produção)
- Pipeline de CI com GitHub Actions
