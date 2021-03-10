(* Module implementing notes from CS 4110 *)

(* De Bruijn Notation is used for expressions *)
type expr = 
  | Index of int
  | Lambda of expr
  | App of expr * expr

let rec string_of_expr (e : expr) : string = 
  match e with 
  | Index n -> string_of_int n 
  | Lambda e1 -> "\\." ^ string_of_expr e1 ^ ""
  | App (e1, e2) -> "(" ^ string_of_expr e1 ^ " " ^ string_of_expr e2 ^ ")"

let rec shift c i e = 
  match e with 
  | Index n -> Index(if n < c then n else n + i)
  | Lambda e -> Lambda (shift (c + 1) i e)
  | App (e1, e2) -> App (shift c i e1, shift c i e2)

let rec subst e e0 m = 
  match e with 
  | Index n -> if n = m then e0 else Index n
  | Lambda e1 -> Lambda (subst e1 (shift 0 1 e0) (m + 1))
  | App (e1, e2) -> App (subst e1 e0 m, subst e2 e0 m)

let beta (e1 : expr) (e2 : expr) : expr = 
  shift 0 (-1) (subst e1 (shift 0 1 e2) 0)

let step (e : expr) : expr = 
  match e with 
  | Index _ -> failwith ("Variable " ^ string_of_expr e ^ "cannot be interpreted.")
  | Lambda _ -> e
  | App (Lambda e1, e2) -> beta e1 e2
  | App _ -> failwith ("Cannot apply non-function " ^ string_of_expr e)

let is_value (e : expr) : bool = 
  match e with 
  | Index _ -> false 
  | App _ -> false
  | Lambda _ -> true 

let rec interpret (e : expr) : expr = 
  if is_value e then e 
  else 
    let () = e |> string_of_expr |> print_endline in 
    let e' = step e in
    interpret e'

let main () = 
  let omega = Lambda (App ((Index 0),(Index 0))) in 
  App(omega, omega) 
  |> interpret 
  |> string_of_expr
  |> print_endline

let () = main ()