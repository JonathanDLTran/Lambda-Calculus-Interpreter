let rec halve lst = 
  match lst with 
  | [] -> [], []
  | h :: [] -> [h], []
  | h1 :: h2 :: t -> 
    let (first, second) = halve t in 
    (h1 :: first, h2 :: second)

let rec merge lst1 lst2 = 
  match lst1, lst2 with 
  | [], [] -> []
  | _, [] -> lst1
  | [], _ -> lst2 
  | h1 :: t1, h2 :: t2 -> 
    if h1 < h2 then h1 :: merge t1 lst2 
    else h2 :: merge lst1 t2

let rec mergesort lst = 
  match lst with 
  | [] -> []
  | [x] -> [x]
  | _ -> let first, second = halve lst in 
    merge (mergesort first) (mergesort second)


let rec partition lst e = 
  match lst with 
  | [] -> [], []
  | h :: t -> 
    let (lt, gt) = partition t e in 
    if h <= e then (h :: lt, gt)
    else (lt, h :: gt)

let rec quicksort lst = 
  match lst with 
  | [] -> []
  | h :: t -> 
    let (first, second) = partition t h in 
    quicksort first @ [h] @ quicksort second