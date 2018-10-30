--Constants
let trival_head = Status { fields      = [ Field (0, 1) 210
                                         , Field (1, 0) 210
                                         , Field (1, 1) 210
                                         , Field (1, 2) 210 ]
                         , concentrate = 213
                         , clothType   = REPAIR
                         , powerCycle  = [1, 0, 1.5, 0.5, 2] }


type Row = Int
type Col = Int
type Damage = Int
data Field = Field (Row, Col) Damage
coordinate :: Field -> (Row,Col)
coordinate (Field (x,y) _) = (x,y)

type SewPower = Float
type PowerCycle = [SewPower]

data ClothType = RAINBOW | REPAIR


data Status = Status { fields      :: [Field]
                     , concentrate :: Int
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
-- act' :: Status -> String -> Field
-- act' status "sewing" = Field (x, y) (110-12)
-- detect (Status a b c d) (x,y) = find (\x -> 

-- Å“K‰ğQÆ
main = do print "oho"
