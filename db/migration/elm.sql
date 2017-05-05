CREATE TABLE `shops` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `shop_id` bigint(20) DEFAULT NULL,
    `address` VARCHAR(100) DEFAULT NULL,
    `latitude` double NOT NULL,
    `longitude` double NOT NULL,
    `phone` VARCHAR(100) DEFAULT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;