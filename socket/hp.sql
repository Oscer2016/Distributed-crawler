DROP DATABASE IF EXISTS `HP`;
CREATE DATABASE `HP`;
USE `HP`;

DROP TABLE IF EXISTS `info`;
CREATE TABLE `info` (
  `id` int(10) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `ip` char(20) DEFAULT NULL,
  `status` enum('21','34','55') DEFAULT NULL COMMENT '21: 工作  34:异常  55: 未工作\n',
  `tasknum` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

ALTER TABLE `info` AUTO_INCREMENT = 0000000000;

DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `url` char(5) NOT NULL,
  `keywords` char(50) NOT NULL,
  `genre` enum('1','2','3') DEFAULT NULL COMMENT '1: 电商  2: 博客 3: 新闻\n',
  `id` int(10) unsigned zerofill NOT NULL,
  `time` datetime DEFAULT NULL,
  `status` enum('5','8','13') DEFAULT NULL COMMENT '5: 运行 8: 等待 13: 完成\n',
  PRIMARY KEY (`url`,`keywords`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `amount`;
CREATE TABLE `amount` (
  `url` char(5) DEFAULT NULL,
  `keywords` char(50) DEFAULT NULL,
  `total` int(11) NOT NULL,
  `genre` enum('1','2','3') DEFAULT NULL COMMENT '1: 电商  2: 博客 3: 新闻\n',
  `time` datetime NOT NULL,
  FOREIGN KEY (`url`) REFERENCES `task` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
