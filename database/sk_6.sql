-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2024-02-22 11:09:27
-- サーバのバージョン： 10.4.32-MariaDB
-- PHP のバージョン: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `sk_6`
--
CREATE DATABASE IF NOT EXISTS `sk_6` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `sk_6`;

GRANT USAGE ON *.* TO `admin`@`localhost` IDENTIFIED BY PASSWORD '*6548C40A208FF1E21D7ED9B546B9CF639D30793C';
GRANT ALL PRIVILEGES ON `sk_6`.* TO `admin`@`localhost`;
-- --------------------------------------------------------

--
-- テーブルの構造 `admins`
--

CREATE TABLE IF NOT EXISTS `admins` (
  `id` char(8) NOT NULL COMMENT '管理者ID',
  `name` varchar(20) NOT NULL COMMENT '管理者名',
  `email` varchar(50) NOT NULL COMMENT 'メールアドレス',
  `password` varchar(100) NOT NULL COMMENT 'パスワード',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `admins`
--

INSERT INTO `admins` (`id`, `name`, `email`, `password`, `created_at`, `updated_at`, `deleted_at`) VALUES
('AD102495', 'admin', 'admin@gmail.com', 'password', '2024-02-14 10:51:38', NULL, NULL);

-- --------------------------------------------------------

--
-- テーブルの構造 `devices`
--

CREATE TABLE IF NOT EXISTS `devices` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'デバイスID',
  `user_id` int(6) NOT NULL COMMENT 'ユーザーID',
  `name` varchar(20) NOT NULL COMMENT 'デバイス名',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時',
  PRIMARY KEY (`id`),
  KEY `fk_devices_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `devices`
--

INSERT INTO `devices` (`id`, `user_id`, `name`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 1, 'MyWindowsPC', '2024-02-11 16:06:13', NULL, NULL),
(2, 2, 'MyMacBookPro', '2024-02-11 16:06:13', NULL, NULL);

-- --------------------------------------------------------

--
-- テーブルの構造 `inquiries`
--

CREATE TABLE IF NOT EXISTS `inquiries` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '問い合わせID',
  `user_id` int(6) NOT NULL COMMENT 'ユーザーID',
  `title` varchar(30) NOT NULL COMMENT 'タイトル',
  `text` varchar(400) NOT NULL COMMENT '本文',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  PRIMARY KEY (`id`),
  KEY `fk_inquiries_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `inquiries`
--

INSERT INTO `inquiries` (`id`, `user_id`, `title`, `text`, `created_at`) VALUES
(1, 2, 'モデル削除について', 'ああああいいいいううううええええおおおお', '2024-02-22 18:59:04');

-- --------------------------------------------------------

--
-- テーブルの構造 `models`
--

CREATE TABLE IF NOT EXISTS `models` (
  `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'モデルID',
  `user_id` int(6) NOT NULL COMMENT 'ユーザーID',
  `name` varchar(20) NOT NULL COMMENT 'モデル名',
  `model_file_name` varchar(30) NOT NULL COMMENT 'モデルファイル名',
  `model_image` varchar(30) DEFAULT NULL COMMENT 'モデル画像',
  `model_info` varchar(400) DEFAULT NULL COMMENT 'モデル詳細',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時',
  PRIMARY KEY (`id`),
  UNIQUE KEY `model_file_name` (`model_file_name`),
  KEY `fk_models_user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `models`
--

INSERT INTO `models` (`id`, `user_id`, `name`, `model_file_name`, `model_image`, `model_info`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 1, 'サンプルモデル', 'sample.obj', 'sample.png', 'サンプルサンプル', '2024-02-21 12:14:57', NULL, NULL);

-- --------------------------------------------------------

--
-- テーブルの構造 `notices`
--

CREATE TABLE IF NOT EXISTS `notices` (
  `id` char(8) NOT NULL COMMENT 'お知らせID',
  `admin_id` char(8) NOT NULL COMMENT '管理者ID',
  `title` varchar(30) NOT NULL COMMENT 'タイトル',
  `text` varchar(200) NOT NULL COMMENT '本文',
  `notice_group_id` int(1) NOT NULL COMMENT '通知グループID',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  PRIMARY KEY (`id`),
  KEY `fk_notices_admin` (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `notices`
--

INSERT INTO `notices` (`id`, `admin_id`, `title`, `text`, `notice_group_id`, `created_at`) VALUES
('1', 'AD102495', 'モデル削除について', 'モデルが削除できないエラーを修正しました。', 3, '2024-02-22 18:59:58');

-- --------------------------------------------------------

--
-- テーブルの構造 `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(6) NOT NULL AUTO_INCREMENT COMMENT 'ユーザーID',
  `name` varchar(20) NOT NULL COMMENT 'ユーザー名',
  `email` varchar(50) NOT NULL COMMENT 'メールアドレス',
  `password` varchar(100) NOT NULL COMMENT 'パスワード',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'test', 'test@gmail.com', 'password', '2024-02-11 16:02:47', NULL, NULL),
(2, '吉川元春', 'kikkawa.motoharu@gmail.com', 'password', '2024-02-11 16:02:47', NULL, NULL);

--
-- ダンプしたテーブルの制約
--

--
-- テーブルの制約 `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `fk_devices_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- テーブルの制約 `inquiries`
--
ALTER TABLE `inquiries`
  ADD CONSTRAINT `fk_inquiries_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- テーブルの制約 `models`
--
ALTER TABLE `models`
  ADD CONSTRAINT `fk_models_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- テーブルの制約 `notices`
--
ALTER TABLE `notices`
  ADD CONSTRAINT `fk_notices_admin` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
