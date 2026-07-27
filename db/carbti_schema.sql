CREATE DATABASE IF NOT EXISTS `carbti`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `carbti`;

CREATE TABLE `manufacturer` (
    `manufacturer_id`   INT             NOT NULL AUTO_INCREMENT,
    `manufacturer_name` VARCHAR(255)    NOT NULL,
    `country`           VARCHAR(255)    NULL,
    `logo_url`          VARCHAR(255)    NULL,
    `official_url`      VARCHAR(255)    NULL,
    PRIMARY KEY (`manufacturer_id`)
);

CREATE TABLE `vehicle` (
    `vehicle_id`      INT           NOT NULL AUTO_INCREMENT,
    `vehicle_name`    VARCHAR(255)  NOT NULL,
    `body_type`       VARCHAR(255)  NOT NULL,
    `car_img`         VARCHAR(255)  NULL,
    `car_description` VARCHAR(255)  NULL,
    `vec_purpose`     VARCHAR(255)  NULL,
    `new_car_url`     VARCHAR(255)  NULL,
    `used_car_url`    VARCHAR(255)  NULL,
    `manufacturer_id` INT           NOT NULL,
    PRIMARY KEY (`vehicle_id`),
    FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturer`(`manufacturer_id`)
);

CREATE TABLE `vehicle_detail` (
    `detail_id`              INT           NOT NULL AUTO_INCREMENT,
    `vehicle_id`              INT           NOT NULL,
    `detail_trim_name`        VARCHAR(255)  NULL,
    `detail_fuel_type`        VARCHAR(255)  NULL,
    `detail_displacement`     INT           NULL,
    `detail_horsepower`       INT           NULL,
    `detail_transmission`     VARCHAR(255)  NULL,
    `detail_drive_type`       VARCHAR(255)  NULL,
    `detail_seat_count`       INT           NULL,
    `detail_base_price`       INT           NULL,
    `detail_fuel_efficiency`  DECIMAL(10,2) NULL,
    PRIMARY KEY (`detail_id`),
    FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle`(`vehicle_id`)
);

CREATE TABLE `option` (
    `option_id`       INT           NOT NULL AUTO_INCREMENT,
    `option_category` VARCHAR(255)  NULL,
    `option_name`     VARCHAR(255)  NULL,
    PRIMARY KEY (`option_id`)
);

CREATE TABLE `vehicle_option` (
    `option_id` INT NOT NULL,
    `detail_id` INT NOT NULL,
    PRIMARY KEY (`option_id`, `detail_id`),
    FOREIGN KEY (`option_id`) REFERENCES `option`(`option_id`),
    FOREIGN KEY (`detail_id`) REFERENCES `vehicle_detail`(`detail_id`)
);

CREATE TABLE `news` (
    `news_id`       INT           NOT NULL AUTO_INCREMENT,
    `title`         VARCHAR(255)  NULL,
    `summary`       VARCHAR(255)  NULL,
    `news_url`      VARCHAR(255)  NULL,
    `news_img`      VARCHAR(255)  NULL,
    `news_category` VARCHAR(255)  NULL,
    `publish_date`  DATE          NULL,
    `vehicle_id`    INT           NULL,
    PRIMARY KEY (`news_id`),
    FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle`(`vehicle_id`)
);

CREATE TABLE `sales_stat` (
    `sales_id`        INT   NOT NULL AUTO_INCREMENT,
    `sales_year`      YEAR  NOT NULL,
    `sales_month`     INT   NOT NULL,
    `sales_count`     INT   NULL,
    `sales_avg_price` INT   NULL,
    `vehicle_id`      INT   NOT NULL,
    PRIMARY KEY (`sales_id`),
    FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle`(`vehicle_id`)
);

CREATE TABLE `car_mbti` (
    `mbti_id`          VARCHAR(10)   NOT NULL,
    `mbti_name`        VARCHAR(255)  NULL,
    `mbti_description` VARCHAR(255)  NULL,
    `mbti_tags`        VARCHAR(255)  NULL,
    PRIMARY KEY (`mbti_id`)
);

CREATE TABLE `car_recommend` (
    `recom_id`       INT           NOT NULL AUTO_INCREMENT,
    `recom_reason`   VARCHAR(255)  NULL,
    `recom_car_rank` INT           NULL,
    `vehicle_id`     INT           NOT NULL,
    `mbti_id`        VARCHAR(10)   NOT NULL,
    PRIMARY KEY (`recom_id`),
    FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle`(`vehicle_id`),
    FOREIGN KEY (`mbti_id`) REFERENCES `car_mbti`(`mbti_id`)
);