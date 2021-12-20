CREATE DATABASE COVID;

USE COVID;
GO

-- CREAR MODELO
CREATE TABLE temp(
	iso_code VARCHAR(100),
	continent VARCHAR(100),
	location VARCHAR(100),
	date VARCHAR(100),
	total_cases VARCHAR(100),
	new_cases VARCHAR(100),
	new_cases_smoothed VARCHAR(100),
	total_deaths VARCHAR(100),
	new_deaths VARCHAR(100),
	new_deaths_smoothed VARCHAR(100),
	total_cases_per_million	VARCHAR(100),
	new_cases_per_million VARCHAR(100),
	new_cases_smoothed_per_million VARCHAR(100),
	total_deaths_per_million VARCHAR(100),
	new_deaths_per_million VARCHAR(100),
	new_deaths_smoothed_per_million VARCHAR(100),
	reproduction_rate VARCHAR(100),
	icu_patients VARCHAR(100),
	icu_patients_per_million VARCHAR(100),
	hosp_patients VARCHAR(100),
	hosp_patients_per_million VARCHAR(100),
	weekly_icu_admissions VARCHAR(100),
	weekly_icu_admissions_per_million VARCHAR(100),
	weekly_hosp_admissions	VARCHAR(100),
	weekly_hosp_admissions_per_million VARCHAR(100),
	new_tests VARCHAR(100),
	total_tests VARCHAR(100),
	total_tests_per_thousand VARCHAR(100),
	new_tests_per_thousand VARCHAR(100),
	new_tests_smoothed VARCHAR(100),
	new_tests_smoothed_per_thousand VARCHAR(100),
	positive_rate VARCHAR(100),
	tests_per_case VARCHAR(100),
	tests_units VARCHAR(100),
	total_vaccinations VARCHAR(100),
	people_vaccinated VARCHAR(100),
	people_fully_vaccinated VARCHAR(100),
	total_boosters VARCHAR(100),
	new_vaccinations VARCHAR(100),
	new_vaccinations_smoothed VARCHAR(100),
	total_vaccinations_per_hundred VARCHAR(100),
	people_vaccinated_per_hundred VARCHAR(100),
	people_fully_vaccinated_per_hundred VARCHAR(100),
	total_boosters_per_hundred VARCHAR(100),
	new_vaccinations_smoothed_per_million VARCHAR(100),
	new_people_vaccinated_smoothed VARCHAR(100),	
	new_people_vaccinated_smoothed_per_hundred VARCHAR(100),
	stringency_index VARCHAR(100),
	population VARCHAR(100),
	population_density VARCHAR(100),
	median_age VARCHAR(100),
	aged_65_older VARCHAR(100),
	aged_70_older VARCHAR(100),
	gdp_per_capita VARCHAR(100),
	extreme_poverty	VARCHAR(100),
	cardiovasc_death_rate VARCHAR(100),
	diabetes_prevalence	VARCHAR(100),
	female_smokers VARCHAR(100),
	male_smokers VARCHAR(100),
	handwashing_facilities VARCHAR(100),
	hospital_beds_per_thousand VARCHAR(100),
	life_expectancy	VARCHAR(100),
	human_development_index	VARCHAR(100),
	excess_mortality_cumulative_absolute VARCHAR(100),
	excess_mortality_cumulative VARCHAR(100),	
	excess_mortality VARCHAR(100),
	excess_mortality_cumulative_per_million VARCHAR(100)
);


CREATE TABLE continent(
	idContinent INT IDENTITY(1,1) PRIMARY KEY,
	name VARCHAR(20) NOT NULL
);

CREATE TABLE country(
	idCountry INT IDENTITY(1,1) PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	iso_code VARCHAR(5) NOT NULL,
	idContinent INT NOT NULL
	FOREIGN KEY (idContinent) REFERENCES continent(idContinent)
	
);

CREATE TABLE fecha(
	idFecha INT IDENTITY(1,1) PRIMARY KEY,
	dia INTEGER NOT NULL,
	mes INTEGER NOT NULL,
	anio INTEGER NOT NULL
);

CREATE TABLE vaccinates_data(
	idVaccnates_data INT IDENTITY(1,1) PRIMARY KEY,
	idFecha INT NOT NULL,
	idCountry INT NOT NULL,
	total_vaccination float,
	people_fully_vaccinated float,
	total_boosters float,
	new_vaccinations float,
	new_vaccinatios_smoothed float,
	total_vaccionations_per_hundred float,
	people_vaccionations_per_hundred float,
	people_fully_vaccnations_per_hundred float,
	total_boosters_per_hundred float,
	new_vaccinations_smoothed_per_million float,
	new_people_vaccinated_smoothed float,
	new_people_vaccinated_smoothed_per_hundred float,
	FOREIGN KEY (idFecha) REFERENCES fecha(idFecha),
	FOREIGN KEY (idCountry) REFERENCES country(idCountry)
	);

CREATE TABLE testunits(
	idTestUnits INT IDENTITY(1,1) PRIMARY KEY,
	test_units VARCHAR(255) 
)


CREATE TABLE reproduction_rate_data(
	idRepoduction_data INT IDENTITY(1,1) PRIMARY KEY,
	idFecha INT NOT NULL,
	idCountry INT NOT NULL,
	idTestUnits INT,
	icu_patints float,
	icu_patientes_per_million float,
	hosp_patients float,
	hosp_patients_per_million float,
	weekly_icu_addmissions float,
	weekly_ico_addmissions_per_million float,
	weekly_hosp_admissions float,
	weekly_hosp_admissions_per_million float,
	new_test float,
	test_units float,
	total_test float,
	total_test_per_thousand float,
	new_test_per_thousand float,
	new_test_smoothed float,
	new_test_smoothed_per_thousand float,
	positive_ate float,
	test_per_case float,
	FOREIGN KEY (idFecha) REFERENCES fecha(idFecha),
	FOREIGN KEY (idCountry) REFERENCES country(idCountry),
	FOREIGN KEY (idTestUnits) REFERENCES testunits(idTestUnits)
);


CREATE TABLE cases_per_day_data(
	idRepoduction_data INT IDENTITY(1,1) PRIMARY KEY,
	idFecha INT NOT NULL,
	idCountry INT NOT NULL,
	total_cases float,
	new_cases float,
	new_cases_smoothed float,
	total_deaths float,
	new_deaths float,
	new_deaths_smoothed float,
	total_cases_per_million float,
	new_cases_per_million float,
	new_cases_smoothed_per_million float,
	total_deaths_per_million float,
	new_deaths_per_million float,
	FOREIGN KEY (idFecha) REFERENCES fecha(idFecha),
	FOREIGN KEY (idCountry) REFERENCES country(idCountry)
);

CREATE TABLE population_index_data(
	idPopulation_index_data INT IDENTITY(1,1) PRIMARY KEY,
	idFecha INT NOT NULL,
	idCountry INT NOT NULL,
	stringency_index float,
	population_desity float,
	median_age float,
	aged_65_older float,
	aged_70_older float,
	gdp_per_capital float,
	extreme_prverty float,
	cordiovasc_death_rate float,
	diabetes_prevalence float,
	female_smokes float,
	male_smokers float,
	handwahing_facilities float,
	hospital_beds_per_thoudand float,
	life_expentancy float,
	human_devolpment_indes float,
	excess_mortality_cumulative_absolute float,
	excess_mortality_cumulative float,
	excess_mortality float,
	excess_moratality_cumlative_million float,
	FOREIGN KEY (idFecha) REFERENCES fecha(idFecha),
	FOREIGN KEY (idCountry) REFERENCES country(idCountry)
);

--  Cargar data
Bulk insert temp 
	From 'C:\Users\User\Documents\Semi2_2\datos-datos.csv' 
	With( Firstrow = 3,        
    FIELDTERMINATOR = ',' ,  
         ROWTERMINATOR = '\n' );

SELECT DISTINCT tests_units FROM temp;
SELECT DISTINCT continent FROM temp;
SELECT DISTINCT iso_code, locations, idContinent FROM temp, continent 
	WHERE continent.name = temp.continent AND continent IS NOT NULL and locations IS NOT NULL;

INSERT INTO testunits(test_units) 
	SELECT DISTINCT tests_units FROM temp;

INSERT INTO continent(name) 
	SELECT DISTINCT continent FROM temp WHERE continent IS NOT NULL;

INSERT INTO country(iso_code, name, idContinent)
	SELECT DISTINCT iso_code, locations, idContinent FROM temp, continent 
		WHERE continent.name = temp.continent AND continent IS NOT NULL and locations IS NOT NULL;

