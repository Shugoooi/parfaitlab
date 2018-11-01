import Data.List

--Constants
trivalHead = Status { fields      = [ Field (0, 1) 210
                                     , Field (1, 0) 210
                                     , Field (1, 1) 210
                                     , Field (1, 2) 210 ]
                     , concentrate = 213
                     , clothType   = REPAIR
                     , powerCycle  = [1, 0, 1.5, 0.5, 2] }

type Row = Int
type Col = Int
type Coordinate = (Row, Col)
type Damage = Int
data Field = Field Coordinate Damage deriving (Show)
coordinate :: Field -> (Row,Col)
coordinate (Field (x,y) _) = (x,y)

type SewPower = Float
type PowerCycle = [SewPower]

data ClothType = RAINBOW | REPAIR
type Concentrate = Int

data Status = Status { fields      :: [Field]
                     , concentrate :: Concentrate
                     , clothType   :: ClothType
                     , powerCycle  :: PowerCycle }

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
takeDamage :: [Field] -> Field -> [Field]
takeDamage fs f = first ++ [takeDamage' (head second) f] ++ tail second
    where (first, second) = break (\x -> coordinate x == coordinate f) fs

takeDamage' :: Field -> Field -> Field
takeDamage' (Field a dx) (Field b dy) = Field a (dx-dy)

updateField :: Status -> [Field] -> Status
updateField status field = status { fields=field }
updateConcentrate :: Status -> Concentrate -> Status
updateConcentrate status concentrate = status { concentrate=concentrate }
-- act' :: Status -> String -> Field
-- act' status "sewing" = Field (x, y) (110-12)
-- detect (Status a b c d) (x,y) = find (\x -> 
detect :: [Field] -> Coordinate -> Maybe Field
detect f c = find (\x -> coordinate x == c) f

-- Å“K‰ğQÆ
main = do print $ detect (fields trivalHead) (1,1)
