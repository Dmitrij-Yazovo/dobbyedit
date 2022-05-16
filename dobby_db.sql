DROP TABLE IF EXISTS `comment`;
DROP TABLE IF EXISTS `postfile`;
DROP TABLE IF EXISTS `post`;
DROP TABLE IF EXISTS `file`;
DROP TABLE IF EXISTS `member`;


DROP TABLE IF EXISTS `member`; 
CREATE TABLE `member` (
	`member_id`	varchar(20)	NOT NULL	PRIMARY KEY,
	`member_email`	varchar(50)	NOT NULL,
	`member_password`	varchar(20)	NOT NULL,
	`member_joindate`	datetime	NOT NULL	DEFAULT now()	COMMENT '가입일',
	`member_status`	tinyint	NOT NULL	DEFAULT 0	COMMENT '0-정상회원 (,1-탈퇴회원)',
	`member_nick`	varchar(20)	NOT NULL
);

DROP TABLE IF EXISTS `post`; 
CREATE TABLE `post` (
	`post_no`	int	NOT NULL	COMMENT '글식별자'	AUTO_INCREMENT,
	`member_id`	varchar(20)	NOT NULL,
	`post_title`	varchar(50)	NOT NULL,
	`post_detail`	varchar(1000)	NOT NULL,
	`post_update`	datetime	NOT NULL	DEFAULT now(),
    
    PRIMARY KEY (`post_no`,`member_id`)
);

DROP TABLE IF EXISTS `comment`; 
CREATE TABLE `comment` (
	`comment_no`	int	NOT NULL	COMMENT '댓글식별자'	AUTO_INCREMENT,
	`member_id`	varchar(20)	NOT NULL,
	`post_no`	int	NOT NULL	COMMENT '글식별자',
	`comment_detail`	varchar(1000)	NOT NULL,
	`comment_update`	datetime	NOT NULL	DEFAULT now(),
    
    PRIMARY KEY (`comment_no`,`member_id`,`post_no`)
);

DROP TABLE IF EXISTS `file`; 
CREATE TABLE `file` (
	`file_no`	int	NOT NULL	AUTO_INCREMENT,
	`member_id`	varchar(20)	NOT NULL,
	`file_name`	varchar(50)	NOT NULL,
	`file_date`	datetime	NOT NULL	DEFAULT now(),
	`file_root`	varchar(1000)	NOT NULL,
    
    PRIMARY KEY (`file_no`,`member_id`)
);

DROP TABLE IF EXISTS `postfile`; 
CREATE TABLE `postfile` (
	`postfile_no`	int	NOT NULL	AUTO_INCREMENT,
	`post_no`	int	NOT NULL	COMMENT '글식별자',
	`member_id`	varchar(20)	NOT NULL,
	`postfile_name`	varchar(50)	NOT NULL,
	`postfile_root`	varchar(1000)	NOT NULL,
    
    PRIMARY KEY (`postfile_no`,`post_no`,`member_id`)
);



ALTER TABLE `post` ADD CONSTRAINT `FK_member_TO_post_1` FOREIGN KEY (
	`member_id`
)
REFERENCES `member` (
	`member_id`
)on delete cascade;

ALTER TABLE `comment` ADD CONSTRAINT `FK_member_TO_comment_1` FOREIGN KEY (
	`member_id`
)
REFERENCES `member` (
	`member_id`
)on delete cascade;

ALTER TABLE `comment` ADD CONSTRAINT `FK_post_TO_comment_1` FOREIGN KEY (
	`post_no`
)
REFERENCES `post` (
	`post_no`
)on delete cascade;

ALTER TABLE `file` ADD CONSTRAINT `FK_member_TO_file_1` FOREIGN KEY (
	`member_id`
)
REFERENCES `member` (
	`member_id`
)on delete cascade;

ALTER TABLE `postfile` ADD CONSTRAINT `FK_post_TO_postfile_1` FOREIGN KEY (
	`post_no`
)
REFERENCES `post` (
	`post_no`
)on delete cascade;

ALTER TABLE `postfile` ADD CONSTRAINT `FK_post_TO_postfile_2` FOREIGN KEY (
	`member_id`
)
REFERENCES `post` (
	`member_id`
)on delete cascade;





DROP PROCEDURE IF EXISTS loopInsert_member;
DROP PROCEDURE IF EXISTS loopInsert_post;
DROP PROCEDURE IF EXISTS loopInsert_comment;
DROP PROCEDURE IF EXISTS loopInsert_file;
DROP PROCEDURE IF EXISTS loopInsert_postfile;



#멤버더미
DELIMITER $$
CREATE PROCEDURE loopInsert_member()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO member(member_id, member_email , member_password, member_joindate, member_status, member_nick)
          VALUES(concat('test',i), concat('이메일@',i), concat('pass',i), now(), default, concat('닉네임',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


# 글더미
DELIMITER $$
CREATE PROCEDURE loopInsert_post()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO post(post_title , post_detail, post_update, member_id)
          VALUES(concat('제목',i), concat('내용',i), now(), concat('test',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


# 댓글더미
DELIMITER $$
CREATE PROCEDURE loopInsert_comment()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO comment(post_no , comment_detail, comment_update, member_id)
          VALUES(i, concat('댓글내용',i), now(), concat('test',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


# 첨부파일더미
DELIMITER $$
CREATE PROCEDURE loopInsert_postfile()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO postfile(post_no , postfile_name, postfile_root, member_id)
          VALUES(i, concat('파일이름',i), concat('경로',i), concat('test',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

# 파일더미
DELIMITER $$
CREATE PROCEDURE loopInsert_file()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO file(file_name , file_date, file_root, member_id)
          VALUES(concat('파일이름',i), now(), concat('닉네임',i), concat('test',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


CALL loopInsert_member;
CALL loopInsert_post;
CALL loopInsert_comment;
CALL loopInsert_file;
CALL loopInsert_postfile;
