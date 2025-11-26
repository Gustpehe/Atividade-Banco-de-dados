from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv
import os

Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'Clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    CPF = Column(String(11), nullable=False, unique=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    senha = Column(String(64), nullable=False)
    classe = Column(String(20), nullable=False, default="cliente")

    agendamentos = relationship("Agendamentos", back_populates="cliente")

    def __str__(self):
        return f"Cliente ID:{self.id} Nome:{self.nome} Idade:{self.idade} CPF:{self.CPF}"


class Especialistas(Base):
    __tablename__ = 'Especialistas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    CRM = Column(Integer, nullable=False, unique=True)
    CPF = Column(String(14), nullable=False, unique=True)
    area = Column(String(60), nullable=False)
    senha = Column(String(30), nullable=False)

    agendamentos = relationship("Agendamentos", back_populates="especialista")

    def __str__(self):
        return f"ID:{self.id} CRM:{self.CRM} área de especialização:{self.area} CPF:{self.CPF}"


class Agendamentos(Base):
    __tablename__ = 'Agendamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("Clientes.id"), nullable=False)
    data = Column(DateTime, nullable=False)
    especialista_id = Column(Integer, ForeignKey("Especialistas.id"), nullable=False)
    local = Column(String(100), nullable=False)

    cliente = relationship("Cliente", back_populates="agendamentos")
    especialista = relationship("Especialistas", back_populates="agendamentos")

    def __str__(self):
        return f"ID:{self.id} Cliente atendido:{self.cliente_id} Horário:{self.data}"
