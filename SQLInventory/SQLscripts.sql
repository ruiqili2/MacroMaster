
### creator update the recipe
CREATE PROCEDURE sp_updateRecipes
      ( 
        IN old_name varchar(50),
        IN new_name varchar(50),
        IN new_vege tinyint(1),
        IN new_description longtext,
        IN new_calories int(11),
        IN new_protein int(11),
        IN new_fat int(11),
        IN new_sodium int(11)
      )
      BEGIN
      START TRANSACTION;
  
      UPDATE schema_recipes  
      SET name = new_name,
      vege = new_vege,
      description = new_description,
      calories = new_calories,
      protein = new_protein,
      fat = new_fat,
      sodium = new_sodium
      WHERE name = old_name;

      COMMIT;
      END;

### creator delete the recipe
CREATE PROCEDURE sp_deleteRecipe
  ( 
        IN recipeName varchar(50)
  )
  BEGIN
  START TRANSACTION;
  
  delete
  from schema_recipes  
  WHERE name = recipeName;

  COMMIT;
  END;

### user unlike the recipe.
CREATE PROCEDURE sp_deleteLikeRecipe
  ( 
    IN userName varchar(50),
    IN recipeName varchar(50)
  )
  BEGIN
  START TRANSACTION;
  
  delete
  from schema_like_recipe  
  WHERE recipeName = recipeName
  AND  userName = userName;

  COMMIT;
  END;

### creator delete the recipe.
CREATE PROCEDURE sp_deleteRecipeRelation
  ( 
    IN recipeName varchar(50)
  )
  BEGIN
  START TRANSACTION;
  
  delete
  from schema_like_recipe  
  WHERE recipeName = recipeName;

  COMMIT;
  END;

### update like_table if user change the recipe name
CREATE PROCEDURE sp_updateLikeRecipeName
  ( 
    IN oldName varchar(50),
    IN recipeName varchar(50)
  )
  BEGIN
  START TRANSACTION;
  
  UPDATE schema_like_recipe  
  SET recipeName = recipeName
  WHERE recipeName = oldName;

  COMMIT;
  END

### update recipes rating
CREATE PROCEDURE sp_updateRecipesRating
  ( 
    IN recipeName varchar(50),
    IN new_rating decimal(4,3)
  )
  BEGIN
  START TRANSACTION;
  
  SELECT rating, rating_num INTO @current, @current_NUM 
  FROM schema_recipes 
  WHERE name = recipeName;
  
  SET @new = (@current * @current_NUM + new_rating) / (@current_NUM + 1);
  
  UPDATE schema_recipes  
  SET rating = @new, rating_num = @current_NUM + 1
  WHERE name = recipeName;

  COMMIT;
  END     



  DECLARE current decimal(4,3);
  DECLARE new decimal(4,3);
  DECLARE current_NUM int;


##############################################################################
#      Database changes in Nov. 4                                            #
#      change like_recipe to foreignkey & foreignkey                         #
#      add tables : recipe_tag, contain_tag                                  #
##############################################################################

### use recipe id instead.
### no longer need change name
DROP PROCEDURE sp_updateLikeRecipeName;

CREATE



### due to databse changes
### alter the procedure
DROP PROCEDURE sp_updateRecipes;
DELIMITER //
CREATE PROCEDURE sp_updateRecipes
      ( 
        IN recipeID varchar(32),
        IN new_name varchar(50),
        IN new_calories int(11),
        IN new_protein int(11),
        IN new_fat int(11),
        IN new_sodium int(11)
      )
      BEGIN
      START TRANSACTION;
  
      UPDATE schema_recipes  
      SET name = new_name,
      calories = new_calories,
      protein = new_protein,
      fat = new_fat,
      sodium = new_sodium
      WHERE rid = recipeID;

      COMMIT;
      END;//

### due to databse changes
### alter the procedure
DROP PROCEDURE sp_deleteLikeRecipe;
DELIMITER //
CREATE PROCEDURE sp_deleteLikeRecipe
  ( 
    IN userID int(11),
    IN recipeID varchar(32)
  )
  BEGIN
  START TRANSACTION;
  
  delete
  from schema_like_recipe  
  WHERE r_id_id = recipeID
  AND  user_id_id = userID;

  COMMIT;
  END;
//
DELIMITER;

### due to databse changes
### alter the procedure
DROP PROCEDURE sp_deleteRecipe;
CREATE PROCEDURE sp_deleteRecipe
  ( 
        IN recipeID varchar(32)
  )
  BEGIN
  START TRANSACTION;
  
  delete
  from schema_recipes  
  WHERE rid = recipeID;

  COMMIT;
  END;
  //


Drop procedure sp_updateRecipesRating
DELIMITER //
CREATE PROCEDURE sp_updateRecipesRating
  ( 
    IN recipeID varchar(32),
    IN new_rating decimal(4,3)
  )
  BEGIN
  START TRANSACTION;
  
  SELECT rating, rating_num INTO @current, @current_NUM 
  FROM schema_recipes 
  WHERE rid = recipeID;
  
  SET @new = (@current * @current_NUM + new_rating) / (@current_NUM + 1);
  
  UPDATE schema_recipes  
  SET rating = @new, rating_num = @current_NUM + 1
  WHERE rid = recipeID;

  COMMIT;
  END     



### due to databse changes
### alter the procedure
DROP PROCEDURE sp_deleteRecipeRelation;
CREATE PROCEDURE sp_deleteRecipeRelation
  ( 
    IN recipeID varchar(32)
  )
  BEGIN
  START TRANSACTION;
  
  delete
  from schema_like_recipe  
  WHERE r_id_id = recipeID;

  COMMIT;
  END;
//
DELIMITER;

#### Get my favorite recipe
CREATE PROCEDURE sp_getUserFavorite
  (
    IN userID int(11)
    )
  BEGIN
  START TRANSACTION;
  
  SELECT sr.rid as ID, sr.name as NAME
  FROM schema_recipes sr
  INNER JOIN schema_like_recipe lr
  ON lr.r_id_id = sr.rid  
  WHERE lr.user_id_id = userID;

  COMMIT;
  END;
//

INSERT INTO schema_recipes_tag (detail)
 SELECT distinct(tag)
 FROM origin_tag



CREATE PROCEDURE sp_getRecipeTags
  (
    IN recipeID varchar(32)
    )

  BEGIN
  START TRANSACTION;

  SELECT rt.id as ID, rt.detail as Detail
  FROM schema_contain_tag ct
  INNER JOin schema_recipes_tag rt
  ON ct.t_id_id = rt.id
  WHERE ct.r_id_id = recipeID;

  commit;
  END;
//

#################################
# Insert data into database     #
#################################
DELIMITER //
INSERT INTO schema_recipes (rid, name, rating, calories, protein, fat, sodium)
  select rid ,title, rating, calories, protein, fat, sodium
  from origin_recipes

INSERT INTO schema_contain_tag (r_id_id, t_id_id)
  select sr.rid, st.id
  from schema_recipes sr
  inner join origin_tag ot
  on sr.name = ot.name
  inner join schema_recipes_tag st
  on ot.tag = st.detail

INSERT INTO schema_recipes_detail (r_id_id, instructions)
  select sr.rid, od.directions
  from origin_directions od
  inner join schema_recipes sr
  on sr.name = od.name

######################################

DELIMITER //
CREATE PROCEDURE sp_deleteRecipeTag
  (
    IN recipeID varchar(32)
    )

  BEGIN
  START TRANSACTION;

  DELETE
  FROM schema_contain_tag
  WHERE r_id_id = recipeID;

  commit;
  END;
//


DELIMITER //
CREATE PROCEDURE sp_deleteRecipeDetail
  (
    IN recipeID varchar(32)
    )

  BEGIN
  START TRANSACTION;

  DELETE
  FROM schema_recipes_detail
  WHERE r_id_id  = recipeID;

  commit;
  END;
//


DELIMITER //
CREATE PROCEDURE sp_updateRecipeDetail
  (
    IN recipeID varchar(32),
    IN ins longtext
  )

    BEGIN
    START TRANSACTION;

    UPDATE schema_recipes_detail
    SET instructions = ins
    WHERE r_id_id  = recipeID;

    commit;
    END;
//

ALTER TABLE Recipes ADD INDEX idx_recipes_cal (calories DESC)
ALTER TABLE Recipes ADD INDEX idx_recipes_rat (rating DESC)
ALTER TABLE Recipes ADD FULLTEXT ftxt_recipes_name (name)






