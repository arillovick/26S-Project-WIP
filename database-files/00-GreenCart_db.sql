DROP DATABASE IF EXISTS `green-cart`;
CREATE DATABASE `green-cart`;
USE `green-cart`;
-- USER
CREATE TABLE User (
UserId INT AUTO_INCREMENT PRIMARY KEY,
Email VARCHAR(100),
FirstName VARCHAR(50),
LastName VARCHAR(50),
PaymentMethod VARCHAR(50),
FamilySize INT,
Notifications BOOLEAN
);
-- GROCERY LIST
CREATE TABLE GroceryList (
ListId INT AUTO_INCREMENT PRIMARY KEY,
OwnerId INT,
Est_total DECIMAL(10, 2),
Budget DECIMAL(10, 2),
Store VARCHAR(60),
Actual_total DECIMAL NOT NULL,
FOREIGN KEY (OwnerId) REFERENCES User(UserId)
);
-- CATEGORY
CREATE TABLE Category (
CategoryId INT AUTO_INCREMENT PRIMARY KEY,
Name varchar(50) NOT NULL,
WasteTip text NOT NULL
);
-- FOOD GLOBAL
CREATE TABLE FoodGlobal (
FoodId INT AUTO_INCREMENT PRIMARY KEY,
CategoryId INT NOT NULL,
Name VARCHAR(50) NOT NULL,
UnitPrice DECIMAL(10,2),
Category VARCHAR(100),
DefaultSealedShelfLife INT,
DefaultOpenShelfLife INT,
FOREIGN KEY (CategoryId) REFERENCES Category(CategoryId)
);
-- PANTRY
CREATE TABLE Pantry (
PantryId INT AUTO_INCREMENT PRIMARY KEY,
OwnerId INT,
FOREIGN KEY (OwnerId) REFERENCES User(UserId)
);
-- GROCERY ITEM
CREATE TABLE GroceryItem (
GroceryItemId INT AUTO_INCREMENT,
GroceryListId INT,
ItemId INT NOT NULL,
Name VARCHAR(50),
Price DECIMAL(10,2) NOT NULL,
Amount INT,
WasBought BOOLEAN NOT NULL,
FOREIGN KEY (ItemId) REFERENCES FoodGlobal(FoodId),
FOREIGN KEY (GroceryListId) REFERENCES GroceryList(ListId)
ON DELETE CASCADE,
PRIMARY KEY (GroceryItemId, GroceryListId)
);
-- PANTRY ITEM
CREATE TABLE PantryItem (
PantryItemId INT AUTO_INCREMENT,
PantryId INT,
StorageLocation VARCHAR(100),
FoodId INT NOT NULL,
DateBought datetime,
ExpirationDate datetime,
FOREIGN KEY (PantryId) REFERENCES Pantry(PantryId)
ON DELETE CASCADE,
FOREIGN KEY (FoodId) REFERENCES FoodGlobal(FoodId),
PRIMARY KEY (PantryItemId, PantryId)
);
-- WASTED FOOD
CREATE TABLE WastedFood (
WastedFoodId INT AUTO_INCREMENT PRIMARY KEY,
UserId INT,
FoodId INT,
Amount INT,
DateThrownOut datetime,
FOREIGN KEY (UserId) REFERENCES User(UserId),
FOREIGN KEY (FoodId) REFERENCES FoodGlobal(FoodId)
);
-- EMPLOYEE
CREATE TABLE Employee (
EmpId INT AUTO_INCREMENT PRIMARY KEY,
Name varchar(50) NOT NULL,
Email varchar(100) NOT NULL,
Position varchar(100)
);
-- AUDIT LOG
CREATE TABLE AuditLog (
LogId INT AUTO_INCREMENT PRIMARY KEY,
UserId INT NOT NULL,
ChangeName text NOT NULL,
Datetime datetime,
Description text,
FOREIGN KEY (UserId) REFERENCES Employee(EmpId)
);
