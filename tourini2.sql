/*
Navicat MySQL Data Transfer

Source Server         : MSQL56
Source Server Version : 50623
Source Host           : localhost:3306
Source Database       : tourini2

Target Server Type    : MYSQL
Target Server Version : 50623
File Encoding         : 65001

Date: 2015-05-11 21:06:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text,
  `body_html` text,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `disabled` tinyint(1) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `post_id` (`post_id`),
  KEY `timestamp` (`timestamp`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------
INSERT INTO `comments` VALUES ('1', 'nice', 'nice', '2015-05-10 19:09:15', null, '2', '3');
INSERT INTO `comments` VALUES ('2', 'nice', 'nice', '2015-05-11 00:46:17', null, '6', '14');

-- ----------------------------
-- Table structure for follows
-- ----------------------------
DROP TABLE IF EXISTS `follows`;
CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `follows2_ibfk_2` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of follows
-- ----------------------------
INSERT INTO `follows` VALUES ('2', '3', '2015-05-09 19:00:10');
INSERT INTO `follows` VALUES ('2', '7', '2015-05-10 17:43:40');
INSERT INTO `follows` VALUES ('3', '2', '2015-05-09 00:55:33');
INSERT INTO `follows` VALUES ('6', '2', '2015-05-09 00:53:43');
INSERT INTO `follows` VALUES ('7', '2', '2015-05-09 00:53:05');
INSERT INTO `follows` VALUES ('8', '2', '2015-05-09 00:46:24');

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
  `location` varchar(45) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of posts
-- ----------------------------
INSERT INTO `posts` VALUES ('1', 'I am happy', '2015-05-08 02:29:43', 'lina222', null, null, '2', '');
INSERT INTO `posts` VALUES ('2', 'yeeeeeel', '2015-05-08 20:48:32', 'lina222', null, null, '2', '');
INSERT INTO `posts` VALUES ('3', 'sadadad', '2015-05-08 21:03:25', 'lina222', null, null, '2', '');
INSERT INTO `posts` VALUES ('4', 'aaaa', '2015-05-08 21:04:36', 'lina222', null, null, '2', '');
INSERT INTO `posts` VALUES ('5', 'sssssss', '2015-05-08 22:15:11', 'lina222', null, null, '2', '');
INSERT INTO `posts` VALUES ('6', 'asa', '2015-05-08 23:00:08', 'kimi444', null, null, '4', '');
INSERT INTO `posts` VALUES ('7', 'imaaaaaa', '2015-05-08 23:01:04', 'kimi444', null, null, '4', '');
INSERT INTO `posts` VALUES ('11', '2222', '2015-05-08 23:35:42', 'bibi777', 'uploads/bibi777/2.jpg', null, '7', '');
INSERT INTO `posts` VALUES ('12', 'aaaaaaaaaaa', '2015-05-09 18:58:20', 'lina222', 'uploads/lina222/ampl_logo_01.png', null, '2', '');
INSERT INTO `posts` VALUES ('13', 'Yes！', '2015-05-10 19:15:22', 'kaka666', 'uploads/kaka666/1.jpg', '<p>Yes！</p>', '6', '');
INSERT INTO `posts` VALUES ('14', 'My God!', '2015-05-11 00:40:09', 'kaka666', 'uploads/kaka666/3.jpg', '<p>My God!</p>', '6', '');
INSERT INTO `posts` VALUES ('15', 'Yes!', '2015-05-11 00:57:57', 'dora333', 'uploads/dora333/1.jpg', '<p>Yes!</p>', '3', '');
INSERT INTO `posts` VALUES ('16', 'I love Java', '2015-05-12 01:04:15', 'lina222', 'uploads/lina222/java.jpg', '<p>I love Java</p>', '2', 'Java, Indonesia');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `location` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `about_me` text,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'hala111', 'hala111', 'New York City, US', null, null);
INSERT INTO `user` VALUES ('2', 'lina222', 'lina222', 'Beijing, China', 'lina', 'Yeahhhhhhhh!!!');
INSERT INTO `user` VALUES ('3', 'dora333', 'dora333', 'Newport, NJ', '', 'Yeah');
INSERT INTO `user` VALUES ('4', 'kimi444', 'kimi444', 'Tokyo, Japan', null, null);
INSERT INTO `user` VALUES ('5', 'koko555', 'koko555', null, null, null);
INSERT INTO `user` VALUES ('6', 'kaka666', 'kaka666', null, null, null);
INSERT INTO `user` VALUES ('7', 'bibi777', 'bibi777', null, null, null);
INSERT INTO `user` VALUES ('8', 'wuqi888', 'wuqi888', null, null, null);
