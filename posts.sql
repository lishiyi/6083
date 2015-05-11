/*
Navicat MySQL Data Transfer

Source Server         : MSQL56
Source Server Version : 50623
Source Host           : localhost:3306
Source Database       : tourini2

Target Server Type    : MYSQL
Target Server Version : 50623
File Encoding         : 65001

Date: 2015-05-10 21:08:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for posts
-- ----------------------------
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `user_name` varchar(45) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `body_html` text,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of posts
-- ----------------------------
INSERT INTO `posts` VALUES ('1', 'I am happy', '2015-05-08 02:29:43', 'lina222', null, null, '2');
INSERT INTO `posts` VALUES ('2', 'yeeeeeel', '2015-05-08 20:48:32', 'lina222', null, null, '2');
INSERT INTO `posts` VALUES ('3', 'sadadad', '2015-05-08 21:03:25', 'lina222', null, null, '2');
INSERT INTO `posts` VALUES ('4', 'aaaa', '2015-05-08 21:04:36', 'lina222', null, null, '2');
INSERT INTO `posts` VALUES ('5', 'sssssss', '2015-05-08 22:15:11', 'lina222', null, null, '2');
INSERT INTO `posts` VALUES ('6', 'asa', '2015-05-08 23:00:08', 'kimi444', null, null, '4');
INSERT INTO `posts` VALUES ('7', 'imaaaaaa', '2015-05-08 23:01:04', 'kimi444', null, null, '4');
INSERT INTO `posts` VALUES ('11', '2222', '2015-05-08 23:35:42', 'bibi777', 'uploads/bibi777/2.jpg', null, '7');
INSERT INTO `posts` VALUES ('12', 'aaaaaaaaaaa', '2015-05-09 18:58:20', 'lina222', 'uploads/lina222/ampl_logo_01.png', null, '2');
INSERT INTO `posts` VALUES ('13', 'Yes！', '2015-05-10 19:15:22', 'kaka666', 'uploads/kaka666/1.jpg', '<p>Yes！</p>', '6');
INSERT INTO `posts` VALUES ('14', 'My God!', '2015-05-11 00:40:09', 'kaka666', 'uploads/kaka666/3.jpg', '<p>My God!</p>', '6');
INSERT INTO `posts` VALUES ('15', 'Yes!', '2015-05-11 00:57:57', 'dora333', 'uploads/dora333/1.jpg', '<p>Yes!</p>', '3');
