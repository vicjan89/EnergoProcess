BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tabel_person" (
	"id"	integer NOT NULL,
	"name"	varchar(40) NOT NULL,
	"electrical_safety_group"	varchar(3) NOT NULL,
	"position_id"	bigint,
	"subdivision_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("subdivision_id") REFERENCES "tabel_subdivision"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("position_id") REFERENCES "tabel_position"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "tabel_position" (
	"id"	integer NOT NULL,
	"name"	varchar(80) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tabel_subdivision" (
	"id"	integer NOT NULL,
	"name"	varchar(10) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tabel_worktype" (
	"id"	integer NOT NULL,
	"work_type"	varchar(4) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tabel_tabelrecord" (
	"id"	integer NOT NULL,
	"date_work"	date NOT NULL,
	"work_time"	real,
	"work_foreman"	bool NOT NULL,
	"harmfulness"	bool NOT NULL,
	"siding"	bool NOT NULL,
	"combination"	real,
	"master_id"	bigint,
	"person_id"	bigint NOT NULL,
	"transferred_id"	bigint,
	"work_type_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("master_id") REFERENCES "tabel_person"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("person_id") REFERENCES "tabel_person"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("work_type_id") REFERENCES "tabel_worktype"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("transferred_id") REFERENCES "tabel_person"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "tabel_brigades" (
	"id"	integer NOT NULL,
	"member_id"	bigint,
	"supervisor_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("member_id") REFERENCES "tabel_person"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("supervisor_id") REFERENCES "tabel_person"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "tabel_person" VALUES (1,'Атрошкин Евгений Леонидович','V',4,1);
INSERT INTO "tabel_person" VALUES (2,'Беспалов Андрей Владимирович','V',3,1);
INSERT INTO "tabel_person" VALUES (3,'Булай Олег Валентинович','V',3,1);
INSERT INTO "tabel_person" VALUES (4,'Быков Михаил Константинович','V',3,1);
INSERT INTO "tabel_person" VALUES (5,'Войтик Сергей Александрович','V',3,1);
INSERT INTO "tabel_person" VALUES (6,'Германов Глеб Сергеевич','V',3,1);
INSERT INTO "tabel_person" VALUES (7,'Голощев Александр Иванович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (8,'Горячко Максим Ростиславович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (9,'Горячко Сергей Ростиславович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (10,'Жаворонков Николай Николаевич','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (11,'Жуков Юрий Сергеевич','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (12,'Жураковский Евгений Фёдорович','III',NULL,NULL);
INSERT INTO "tabel_person" VALUES (13,'Ионов Александр Анатольевич','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (14,'Коваленко Евгений Анатольевич','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (15,'Кучко Дмитрий Антонович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (16,'Лабацевич Владислав Сергеевич','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (17,'Литвинович Егор Анатольевич','V',3,1);
INSERT INTO "tabel_person" VALUES (18,'Масалов Юрий Николаевич','V',3,1);
INSERT INTO "tabel_person" VALUES (19,'Мастыко Владислав Валентинович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (20,'Метла Сергей Леонидович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (21,'Пашкевич Александр Александрович','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (22,'Петрачков Игорь Эдуардович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (23,'Поляков Андрей Викторович','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (24,'Ремберг Александр Сергеевич','III',NULL,NULL);
INSERT INTO "tabel_person" VALUES (25,'Саулич Алексей Петрович','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (26,'Саулич Сергей  Петрович','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (27,'Семененков Александр Сергеевич','III',NULL,NULL);
INSERT INTO "tabel_person" VALUES (28,'Семененков Игорь Александрович','V',3,1);
INSERT INTO "tabel_person" VALUES (29,'Сенькин Андрей Владимирович','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (30,'Тымуль Максим Игнатьевич','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (31,'Умецкий Евгений Анатольевич','III',NULL,NULL);
INSERT INTO "tabel_person" VALUES (32,'Хмелевский Вячеслав Игоревич','IV',NULL,NULL);
INSERT INTO "tabel_person" VALUES (33,'Хуртов Денис Иванович','V',3,1);
INSERT INTO "tabel_person" VALUES (34,'Чернов Илья Олегович','V',4,1);
INSERT INTO "tabel_person" VALUES (35,'Шерегов Павел Петрович','III',NULL,NULL);
INSERT INTO "tabel_person" VALUES (36,'Януш Виктор Михайлович','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (37,'Яроцкий Алексей Леонардович','V',NULL,NULL);
INSERT INTO "tabel_person" VALUES (38,'Шидловский Артём Сергеевич','II',NULL,NULL);
INSERT INTO "tabel_position" VALUES (1,'начальник');
INSERT INTO "tabel_position" VALUES (2,'заместитель начальника');
INSERT INTO "tabel_position" VALUES (3,'мастер');
INSERT INTO "tabel_position" VALUES (4,'старший мастер');
INSERT INTO "tabel_position" VALUES (5,'инженер');
INSERT INTO "tabel_position" VALUES (6,'техник');
INSERT INTO "tabel_position" VALUES (7,'водитель автомобиля');
INSERT INTO "tabel_position" VALUES (8,'электромонтёр по ремонту аппаратуры релейной защиты');
INSERT INTO "tabel_subdivision" VALUES (1,'СРЗАИ');
INSERT INTO "tabel_subdivision" VALUES (2,'СОТЭиОТ');
INSERT INTO "tabel_worktype" VALUES (1,'В');
INSERT INTO "tabel_worktype" VALUES (2,'О');
INSERT INTO "tabel_worktype" VALUES (3,'Ук');
INSERT INTO "tabel_worktype" VALUES (4,'Б');
INSERT INTO "tabel_worktype" VALUES (5,'Д/Д');
INSERT INTO "tabel_worktype" VALUES (6,'Д/О');
INSERT INTO "tabel_worktype" VALUES (7,'А');
INSERT INTO "tabel_worktype" VALUES (8,'МО');
INSERT INTO "tabel_worktype" VALUES (9,'У');
INSERT INTO "tabel_tabelrecord" VALUES (1,'2023-01-01',NULL,0,0,0,NULL,4,4,NULL,1);
INSERT INTO "tabel_tabelrecord" VALUES (2,'2023-01-02',NULL,0,0,0,NULL,4,13,NULL,1);
INSERT INTO "tabel_tabelrecord" VALUES (3,'2023-01-03',8.25,0,0,0,NULL,4,13,NULL,NULL);
INSERT INTO "tabel_brigades" VALUES (1,4,4);
INSERT INTO "tabel_brigades" VALUES (2,13,4);
INSERT INTO "tabel_brigades" VALUES (3,38,4);
INSERT INTO "tabel_brigades" VALUES (4,11,6);
CREATE INDEX IF NOT EXISTS "tabel_tabel_master_id_1ed4d6f7" ON "tabel_tabelrecord" (
	"master_id"
);
CREATE INDEX IF NOT EXISTS "tabel_tabel_person_id_76b709e3" ON "tabel_tabelrecord" (
	"person_id"
);
CREATE INDEX IF NOT EXISTS "tabel_tabel_transferred_id_7f021d5e" ON "tabel_tabelrecord" (
	"transferred_id"
);
CREATE INDEX IF NOT EXISTS "tabel_tabel_work_type_id_380eb62e" ON "tabel_tabelrecord" (
	"work_type_id"
);
CREATE INDEX IF NOT EXISTS "tabel_person_position_id_542c4485" ON "tabel_person" (
	"position_id"
);
CREATE INDEX IF NOT EXISTS "tabel_person_subdivision_id_991eb384" ON "tabel_person" (
	"subdivision_id"
);
CREATE INDEX IF NOT EXISTS "tabel_brigades_member_id_b5688dfd" ON "tabel_brigades" (
	"member_id"
);
CREATE INDEX IF NOT EXISTS "tabel_brigades_supervisor_id_71aef255" ON "tabel_brigades" (
	"supervisor_id"
);
COMMIT;
