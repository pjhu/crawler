CREATE TABLE `users` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `url_token` VARCHAR(100) NOT NULL,
    `name` VARCHAR(100) DEFAULT NULL,
    `gender` INT(1) DEFAULT NULL,
    `following_count` int(10) DEFAULT NULL,
    `follower_count` int(10) DEFAULT NULL,
    `following_columns_count` int(10) DEFAULT NULL,
    `following_topic_count` int(10) DEFAULT NULL,
    `articles_count` int(10) DEFAULT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;