CREATE TABLE acoes_sustentaveis (
id INT AUTO_INCREMENT PRIMARY KEY, -- CORRIGIDO: Garante que o ID tenha o tipo INT
descricao VARCHAR(255) NOT NULL,
categoria VARCHAR(100),
impacto VARCHAR(50),
data DATE
);

CREATE TABLE usuarios (
 id INT AUTO_INCREMENT PRIMARY KEY, -- CORRIGIDO: Garante que o ID tenha o tipo INT
 usuario VARCHAR(50) NOT NULL UNIQUE,
 senha VARCHAR(50) NOT NULL
);

-- Para que a funcionalidade de LOGIN funcione (Missão 8), 
-- você DEVE executar a seguinte instrução após criar as tabelas:

INSERT INTO usuarios (usuario, senha) VALUES ('admin', '123');

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Root'; 
FLUSH PRIVILEGES;