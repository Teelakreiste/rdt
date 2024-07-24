CREATE DATABASE IF NOT EXISTS dbrdt;

USE dbrdt;

DROP TABLE Trabajador_labores;
DROP TABLE Labores;
DROP TABLE Trabajadores;

CREATE TABLE IF NOT EXISTS Trabajadores (
    cedula INT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_ingreso DATE,
    tipo_trabajador VARCHAR(50),
    finca VARCHAR(100),
    eps VARCHAR(100),
    fondo_pensiones VARCHAR(100),
    fondo_cesantias VARCHAR(100),
    salario DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Labores (
    identificador INT PRIMARY KEY,
    finca VARCHAR(100),
    lote VARCHAR(100),
    valor DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Trabajador_labores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE,
    cantidad INT,
    id_trabajador INT,
    id_labor INT,
    FOREIGN KEY (id_trabajador) REFERENCES Trabajadores(cedula),
    FOREIGN KEY (id_labor) REFERENCES Labores(identificador)
);