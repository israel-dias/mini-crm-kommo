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
