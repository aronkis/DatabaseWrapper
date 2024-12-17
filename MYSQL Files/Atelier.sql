DROP DATABASE IF EXISTS Atelier;
CREATE DATABASE Atelier;
USE Atelier;

CREATE TABLE Persoana (
    id INT PRIMARY KEY,
    nume VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    adresa VARCHAR(200)
);

-- Populate Persoana
INSERT INTO Persoana (id, nume, email, adresa) 
VALUES
(1, 'Ion Popescu', 'ion.popescu@example.com', 
 'Str. Unirii, nr. 10, Bucuresti'),
(2, 'Maria Ionescu', 'maria.ionescu@example.com', 
 'Str. Victoriei, nr. 5, Cluj-Napoca'),
(3, 'Andrei Gheorghiu', 'andrei.gheorghiu@example.com', 
 'Bdul. Decebal, nr. 15, Timisoara'),
(4, 'Elena Marinescu', 'elena.marinescu@example.com', 
 'Str. Lalelelor, nr. 20, Constanta'),
(5, 'Gabriel Dumitru', 'gabriel.dumitru@example.com', 
 'Bdul. Magheru, nr. 30, Bucuresti'),
(6, 'Mihai Georgescu', 'mihai.georgescu@email.com', 
 'Strada Tineretului, Nr. 5, Ploiesti'),
(7, 'Elena Vasilescu', 'elena.vasilescu@email.com', 
 'Bdul. Unirii, Nr. 32, Timisoara'),
(11, 'Alex Enache', 'Alex.Enache@email.com', 
 'Strada Principale, Nr. 5, Arad'),
(17, 'Robert Purcar', 'Robert.Purcar@email.com', 
 'Strada Siretului, Nr. 32, Baia Mare');

CREATE TABLE Deviz (
    id_d INT PRIMARY KEY,
    data_introducere DATE NOT NULL,
    aparat VARCHAR(100) NOT NULL,
    simptome TEXT NOT NULL,
    defect TEXT,
    data_constatare DATE DEFAULT NULL,
    data_finalizare DATE DEFAULT NULL,
    durata INT,
    manopera_ora DECIMAL(10, 2),
    total DECIMAL(10, 2),
    id_client INT NOT NULL,
    id_depanator INT NOT NULL,
    CONSTRAINT fk_deviz_client FOREIGN KEY (id_client) 
        REFERENCES Persoana(id),
    CONSTRAINT fk_deviz_depanator FOREIGN KEY (id_depanator) 
        REFERENCES Persoana(id)
);

-- Populate Deviz
INSERT INTO Deviz (id_d, data_introducere, aparat, simptome, defect, 
                   data_constatare, data_finalizare, durata, manopera_ora,
                   total, id_client, id_depanator) 
VALUES
(1, '2022-10-01', 'Laptop Dell', 'Nu se deschide', 'Placa video defecta', 
 '2022-02-20', '2022-02-23', 10, 50, 720, 3, 1),
(2, '2024-02-20', 'Laptop Dell', 'Nu se porneste', 'Baterie defecta', 
 '2024-02-21', '2024-02-24', 10, 50, 700, 3, 1),
(3, '2024-02-24', 'Telefon Samsung', 'Ecran spart', 'Ecran defect', 
 '2024-02-25', '2024-02-27', 8, 60, 600, 4, 2),
(4, '2024-03-03', 'Frigider Whirlpool', 'Zgomot din spate', 'Lipseste un surub', 
 '2024-03-04', '2024-03-04', 3, 55, 205, 5, 1),
(5, '2024-03-14', 'Masina de spalat Bosch', 'Nu se inschide usa', 'Lipsesc doua suruburi', 
 '2024-03-15', '2024-03-17', 3, 55, 225, 6, 2),
(6, '2024-09-10', 'Telefon Samsung', 'Nu funcitoneaza touch-ul', 'Ecran defect', 
 '2024-09-11', '2024-09-15', 8, 60, 600, 7, 1);

CREATE TABLE Piesa (
    id_p INT PRIMARY KEY,
    descriere VARCHAR(255) NOT NULL,
    fabricant VARCHAR(100) NOT NULL,
    cantitate_stoc INT NOT NULL CHECK (cantitate_stoc >= 0),
    pret_c DECIMAL(10, 2) NOT NULL,
    CONSTRAINT unique_descriere_fabricant UNIQUE (descriere, fabricant)
);

-- Populate Piesa
INSERT INTO Piesa (id_p, descriere, fabricant, cantitate_stoc, pret_c) VALUES
(1, 'Baterie Laptop Dell', 'Dell', 5, 200),
(2, 'Placa video NVIDIA GeForce GTX 1050', 'NVIDIA', 10, 160),
(3, 'Ecran AMOLED Samsung Galaxy S21', 'Samsung', 15, 150),
(4, 'Compresor frigorific Whirlpool 200W', 'Whirlpool', 8, 220),
(5, 'Mecanism usa masina de spalat Bosch', 'Bosch', 12, 220),
(6, 'Surub pentru compresor Whirlpool', 'Whirlpool', 12, 30),
(7, 'Surub pentru usa masina de spalat Bosch', 'Bosch', 12, 5);

CREATE TABLE Piesa_Deviz (
    id_d INT NOT NULL,
    id_p INT NOT NULL,
    cantitate INT NOT NULL CHECK (cantitate > 0),
    pret_r DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_d, id_p),
    CONSTRAINT fk_piesa_deviz_deviz FOREIGN KEY (id_d) REFERENCES Deviz(id_d),
    CONSTRAINT fk_piesa_deviz_piesa FOREIGN KEY (id_p) REFERENCES Piesa(id_p)
);

-- Populate Piesa_Deviz
INSERT INTO Piesa_Deviz (id_d, id_p, cantitate, pret_r) VALUES
(1, 1, 1, 220),
(2, 2, 1, 180),
(3, 3, 1, 120),
(4, 6, 1, 40),
(5, 7, 2, 8),
(6, 3, 1, 120);

ALTER TABLE Persoana
    MODIFY adresa VARCHAR(200);

ALTER TABLE Persoana
    ADD CONSTRAINT chk_email_format CHECK (CHAR_LENGTH(email) >= 10 
                                    AND LOCATE('@', email) > 0);

ALTER TABLE Deviz
    ADD CONSTRAINT chk_data_finalizare CHECK (data_finalizare IS NULL OR 
                                              data_constatare IS NOT NULL);