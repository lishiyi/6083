/*
Navicat MySQL Data Transfer

Source Server         : MSQL56
Source Server Version : 50623
Source Host           : localhost:3306
Source Database       : tourini2

Target Server Type    : MYSQL
Target Server Version : 50623
File Encoding         : 65001

Date: 2015-05-03 17:54:06
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for follows2
-- ----------------------------
DROP TABLE IF EXISTS `follows2`;
CREATE TABLE `follows2` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `follows2_ibfk_2` (`followed_id`),
  CONSTRAINT `follows2_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `user2` (`user_id`),
  CONSTRAINT `follows2_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `user2` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of follows2
-- ----------------------------

-- ----------------------------
-- Table structure for user2
-- ----------------------------
DROP TABLE IF EXISTS `user2`;
CREATE TABLE `user2` (
  `user_id` int(8) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user2
-- ----------------------------
INSERT INTO `user2` VALUES ('1', 'hala111', 'hala111');
INSERT INTO `user2` VALUES ('2', 'lina222', 'lina222');
INSERT INTO `user2` VALUES ('3', 'Dora333', 'Dora333');
INSERT INTO `user2` VALUES ('4', 'Kimi444', 'Kimi444');
INSERT INTO `user2` VALUES ('5', 'Koko555', 'Koko555');
INSERT INTO `user2` VALUES ('6', 'Kaka666', 'Kaka666');
