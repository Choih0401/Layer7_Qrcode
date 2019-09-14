# Layer7_Qrcode
> Date : 2019.05.20 ~ 2019.05.31  
Platfrom : flask, mysql

# Procedure01
```sql
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_submit`(
    IN p_uid INT(40),
    IN p_time VARCHAR(1000),
    IN p_input VARCHAR(1000)
)
BEGIN
    DECLARE p_statue varchar(100) default 'Wrong';
    if ( select exists (select * from flag where answer = p_input) ) THEN
        SET p_statue = 'overload';
        if ( select exists (select * from log where uid = p_uid AND input = p_input) ) THEN


        	insert into log
            (
                uid,
                time,
                input,
                statue
            )
            values
            (
                p_uid,
                p_time,
                p_input,
                p_statue
            );

        ELSE

            UPDATE tbl_user SET score = score + 1 where user_id = p_uid;


            SET p_statue = 'success';
            insert into log
            (
                uid,
                time,
                input,
                statue
            )
            values
            (
                p_uid,
                p_time,
                p_input,
                p_statue
            );

        END IF;

    ELSE
        SET p_statue = 'Wrong';


        insert into log
        (
            uid,
            time,
            input,
            statue
        )
        values
        (
            p_uid,
            p_time,
            p_input,
            p_statue
        );


    END IF;



END$$
DELIMITER ;
```

# Procedure02
```sql
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_result`(
    IN p_uid INT(40),
    IN p_input VARCHAR(1000)
)
BEGIN
    DECLARE p_statue varchar(100) default 'Wrong';
    if ( select exists (select * from flag where answer = p_input) ) THEN
        if ( select exists (select * from log where uid = p_uid and input = p_input AND statue = 'overload') ) THEN

            select 'Already solve';

        ELSE

            select 'Correct';

        END IF;

    ELSE

        select 'Wrong';


    END IF;



END$$
DELIMITER ;
```

# Procedure03
```sql
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(1000),
    IN p_username VARCHAR(1000),
    IN p_password VARCHAR(1000)
)
BEGIN
    if ( select exists (select * from tbl_user where user_username = p_username) ) THEN

        select 'Username Exists !!';

    ELSE

        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );

    END IF;
END$$
DELIMITER ;
```

# Procedure04
```sql
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_score`(
IN p_uid INT(40)
)
BEGIN
    select score from tbl_user where user_id = p_uid;
END$$
DELIMITER ;
```

# Procedure05
```sql
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(1000)
)
BEGIN
    select * from tbl_user where user_username = p_username;
END$$
DELIMITER ;
```
