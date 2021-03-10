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

let beta (v1 : expr) (v2 : expr) : expr = 
  match v1 with 
  | Lambda e1 -> shift 0 (-1) (subst e1 (shift 0 1 v2) 0)
  | _ -> failwith( "Cannot Beta Substutute into non Function " ^ string_of_expr v1)

let is_value (e : expr) : bool = 
  match e with 
  | Index _ -> false 
  | App _ -> false
  | Lambda _ -> true 

let rec step (e : expr) : expr = 
  match e with 
  | Index _ -> failwith ("Variable " ^ string_of_expr e ^ "cannot be interpreted.")
  | Lambda _ -> failwith ("Lambda expressions do not step " ^ string_of_expr e)
  | App (v1, v2) when (is_value v1) && (is_value v2) -> beta v1 v2
  | App (e1, e2) when not (is_value e1) -> App (interpret e1, e2)
  | App (e1, e2) when not (is_value e2) -> App (e1, interpret e2)
  | App _ -> failwith ("Cannot apply non-function " ^ string_of_expr e)

and interpret (e : expr) : expr = 
  if is_value e then e 
  else 
    let () = e |> string_of_expr |> print_endline in 
    let e' = step e in
    interpret e'

let main () = 
  let first = Lambda (App ((Index 0),(Index 0))) in 
  let omega = App(first, first) in
  let f = Lambda (Lambda (Index 1)) in 
  let g = Lambda (Index 0) in 
  App(App(f, g), omega) 
  |> interpret 
  |> string_of_expr
  |> print_endline

let () = main ()