-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2024-02-14 02:52:44
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

-- --------------------------------------------------------

--
-- テーブルの構造 `admins`
--

CREATE TABLE `admins` (
  `id` char(8) NOT NULL COMMENT '管理者ID',
  `name` varchar(20) NOT NULL COMMENT '管理者名',
  `email` varchar(50) NOT NULL COMMENT 'メールアドレス',
  `password` varchar(100) NOT NULL COMMENT 'パスワード',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時'
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

CREATE TABLE `devices` (
  `id` int(10) NOT NULL COMMENT 'デバイスID',
  `user_id` int(6) NOT NULL COMMENT 'ユーザーID',
  `name` varchar(20) NOT NULL COMMENT 'デバイス名',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `devices`
--

INSERT INTO `devices` (`id`, `user_id`, `name`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 1, 'MyWindowsPC', '2024-02-11 16:06:13', NULL, NULL),
(2, 2, 'MyMacBookPro', '2024-02-11 16:06:13', NULL, NULL);

-- --------------------------------------------------------

--
-- テーブルの構造 `models`
--

CREATE TABLE `models` (
  `id` int(10) NOT NULL COMMENT 'モデルID',
  `user_id` int(6) NOT NULL COMMENT 'ユーザーID',
  `name` varchar(20) NOT NULL COMMENT 'モデル名',
  `file_name` varchar(30) NOT NULL COMMENT 'ファイル名',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `models`
--

INSERT INTO `models` (`id`, `user_id`, `name`, `file_name`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 1, 'サンプルモデル', 'sample.obj', '2024-02-11 16:04:34', NULL, NULL),
(2, 2, '羽柴秀吉モデル', 'hideyoshi.obj', '2024-02-11 16:04:34', NULL, NULL);

-- --------------------------------------------------------

--
-- テーブルの構造 `users`
--

CREATE TABLE `users` (
  `id` int(6) NOT NULL COMMENT 'ユーザーID',
  `name` varchar(20) NOT NULL COMMENT 'ユーザー名',
  `email` varchar(50) NOT NULL COMMENT 'メールアドレス',
  `password` varchar(100) NOT NULL COMMENT 'パスワード',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `updated_at` datetime DEFAULT NULL COMMENT '更新日時',
  `deleted_at` datetime DEFAULT NULL COMMENT '削除日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- テーブルのデータのダンプ `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'test', 'test@gmail.com', 'password', '2024-02-11 16:02:47', NULL, NULL),
(2, '吉川元春', 'kikkawa.motoharu@gmail.com', 'password', '2024-02-11 16:02:47', NULL, NULL);

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_devices_user` (`user_id`);

--
-- テーブルのインデックス `models`
--
ALTER TABLE `models`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `file_name` (`file_name`),
  ADD KEY `fk_models_user` (`user_id`);

--
-- テーブルのインデックス `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'デバイスID', AUTO_INCREMENT=3;

--
-- テーブルの AUTO_INCREMENT `models`
--
ALTER TABLE `models`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT COMMENT 'モデルID', AUTO_INCREMENT=3;

--
-- テーブルの AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(6) NOT NULL AUTO_INCREMENT COMMENT 'ユーザーID', AUTO_INCREMENT=3;

--
-- ダンプしたテーブルの制約
--

--
-- テーブルの制約 `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `fk_devices_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- テーブルの制約 `models`
--
ALTER TABLE `models`
  ADD CONSTRAINT `fk_models_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
