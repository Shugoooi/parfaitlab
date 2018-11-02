module SomeSewing where

import Data.List

--Constants
baseDamage = [12..18]
trivalHead = Status { fields      = [ Field (0, 1) 210
                                    , Field (1, 0) 210
                                    , Field (1, 1) 210
                                    , Field (1, 2) 210 ]
                    , concentrate = 213
                    , clothType   = REPAIR
                    , powerCycle  = [ 1, 0, 1.5, 0.5, 2 ] 
                    }

type Row = Int
type Col = Int
type Coordinate = (Row, Col)
type Damage = Int
data Field = Field Coordinate Damage deriving (Show)
type Fields = [Field]
coordinate :: Field -> (Row,Col)
coordinate (Field (x,y) _) = (x,y)

type SewPower = Float
type PowerCycle = [SewPower]

data ClothType = RAINBOW | REPAIR deriving Show
show RAINBOW = "RAINBOW"
show REPAIR  = "REPAIR"

type Concentrate = Int

data Status = Status { fields      :: Fields
                     , concentrate :: Concentrate
                     , clothType   :: ClothType
                     , powerCycle  :: PowerCycle
                     } deriving (Show)

data Effect = TakeDamage
            | MentalConcentration
            | PowerShift

data Skill = Skill { skillName    :: String
                   , effect       :: Effect
                   , consumption  :: Int }


-- s“®
-- act :: Status -> Skill -> Status
act :: Field -> String -> Field
act (Field (x, y) 110) "sewing" = Field (x, y) (110-12)

takeDamage :: Status -> Field -> Status
takeDamage s f = updateField s $ takeDamage' (fields s) f

takeDamage' :: Fields -> Field -> Fields
takeDamage' fs f = first ++ [takeDamage'' (head second) f] ++ tail second
    where (first, second) = break (\x -> coordinate x == coordinate f) fs
{-
takeDamage' :: Fields -> [Field] -> [Fields]
takeDamage' fs f = first ++ [takeDamage'' (head second) f] ++ tail second
    where (first, second) = break (\x -> coordinate x == coordinate f) fs
-}

takeDamage'' :: Field -> Field -> Field
takeDamage'' (Field a dx) (Field b dy) = Field a (dx-dy)

updateField :: Status -> Fields -> Status
updateField status field = status { fields=field }
updateConcentrate :: Status -> Concentrate -> Status
updateConcentrate status concentrate = status { concentrate=concentrate }
-- act' :: Status -> String -> Field
-- act' status "sewing" = Field (x, y) (110-12)
detectField :: Coordinate -> Fields -> Maybe Field
detectField c = find (\x -> coordinate x == c)
applyDamage :: Coordinate -> [Damage] -> [Field]
applyDamage = (<$>) (<$>) Field


-- Å“K‰ğQÆ
-- main = do print $ takeDamage trivalHead (Field (1,1) 100)
main = do print ( takeDamage <$> [trivalHead] <*> applyDamage (1,1) [12..18] )

