type ctx = (string * lambda) list

and lambda = 
  | Int of int 
  | Plus of lambda * lambda 
  | Let of string * lambda * lambda 
  | Var of string 
  | Abs of string * lambda 
  | App of lambda * lambda
  | DynCtx of ctx
  | Lookup of string * string 
  | Update of string * lambda * string 


type value = 
  | VInt of int
  | VAbs of string * lambda

let rec expr_to_str expr = 
  match expr with 
  | Int n -> string_of_int n
  | Plus(l, r) -> "(" ^ expr_to_str l ^  " + " ^ expr_to_str r ^ ")"
  | Var x -> x 
  | Abs(x, e) -> "fun " ^ x ^ " -> " ^ expr_to_str e
  | App(e1, e2) -> "(" ^ expr_to_str e1 ^ ") (" ^ expr_to_str e2 ^ ")"
  | Let(x, e1, e2) -> failwith "Lets need to already have been desugared"
  | DynCtx _ -> "{DynCtx}"
  | Lookup(ctx, x) -> "(lookup " ^ ctx ^ " " ^ x ^ ")"
  | Update(ctx, v, x) -> "(update " ^ ctx ^ " " ^ expr_to_str v ^ " " ^ x ^ ")"


let val_to_str value = 
  match value with 
  | VInt n -> string_of_int n
  | VAbs(x, e) -> "fun " ^ x ^ " -> " ^ expr_to_str e

let rec fv expr = 
  match expr with 
  | Int _ -> []
  | Var x -> [x]
  | App(e1, e2) -> fv e1 @ fv e2 
  | Plus(e1, e2) -> fv e1 @ fv e2 
  | Abs(x, e) ->  List.filter (fun elt -> elt <> x) (fv e)
  | Let(v, f, s) -> failwith "Lets need to already have been desugared"
  | DynCtx _ -> failwith "No Dynamic Context Handling"

let gen_new_var = 
  let count = ref 0 in 
  fun () -> incr count; "x_" ^ string_of_int !count

(* Substitute e1 for x in e2 = e2{e1/x} *)
let rec subst x e1 e2 = 
  match e2 with 
  | Int _ -> e2 
  | Var y -> if y = x then e1 else e2 
  | App(l, r) -> App(subst x e1 l, subst x e1 r)
  | Plus(l, r) -> Plus(subst x e1 l, subst x e1 r)
  | Let(v, f, s) -> failwith "Lets need to already have been desugared"
  | Abs(y, e0) -> begin 
      if y = x then e2 
      else if y <> x && not (List.mem y (fv e1)) then Abs(y, subst x e1 e0)
      else 
        let z = gen_new_var () in 
        let () = assert (y <> x); assert (z <> x); assert (not (List.mem z (fv e1))); assert (not (List.mem z (fv e0))) in
        Abs(z, subst x e1 (subst y (Var z) e0))
    end 
  | DynCtx _ -> failwith "No Dynamic Context Handling"

(* We can decompose let x = e1 in e2 as *lambda x. e1) e2 *)
let rec eval expr print = 
  let () = if print then expr |> expr_to_str |> print_endline else () in 
  match expr with 
  | Int n -> VInt n
  | Plus (l, r) -> begin 
      match eval l print, eval r print with
      | VInt i1, VInt i2 -> VInt (i1 + i2)
      | _ -> failwith "Cannot add together non-ints"
    end
  | Let (v, e1, e2) -> failwith "Lets need to already have been desugared"
  | Abs(v, e) -> VAbs(v, e)
  | App(e1, e2) -> begin
      match eval e1 print with 
      | VAbs(x, e3) -> 
        let beta = (subst x e2 e3) in eval beta print
      | _ -> failwith "First term in Application must be a function."
    end 
  | Var x -> failwith "Vars cannot be evaluated by themselves"
  | DynCtx _ -> failwith "No Dynamic Context Handling"

let rec remove_lets expr = 
  match expr with 
  | Int _ -> expr 
  | Var _ -> expr 
  | Plus(l, r) -> Plus(remove_lets l, remove_lets r)
  | Abs(v, e) -> Abs(v, remove_lets e)
  | App(l, r) -> App(remove_lets l, remove_lets r) 
  | Let(x, f, s) -> (App (Abs(x, remove_lets s), remove_lets f))
  | DynCtx _ -> failwith "No Dynamic Context Handling"

let rec translate_to_dynamic expr = 
  match expr with 
  | Int n -> fun ctx -> Int n
  | Var x -> fun ctx -> begin  
      match ctx with 
      | DynCtx dynctx -> begin
          match List.assoc_opt x dynctx with 
          | Some value -> value 
          | None -> failwith("Unbound Variable Name " ^ x ^ " in Lambda Term.")
        end
      | _ -> failwith "Not a Dynamic Context"
    end 
  | App(e1, e2) -> begin 
      fun ctx -> 
        App(App(translate_to_dynamic e1 ctx, translate_to_dynamic e2 ctx), ctx)
    end
  | Plus(e1, e2) ->  begin 
      fun ctx -> 
        App(Plus(translate_to_dynamic e1 ctx, translate_to_dynamic e2 ctx), ctx)
    end
  | Abs(x, e) -> begin 
      let v = gen_new_var () in 
      let t = gen_new_var () in 
      fun ctx -> 
        match ctx with 
        | DynCtx dynctx -> begin
            Abs(v, Abs(t, translate_to_dynamic e (DynCtx((x, Var(v))::List.remove_assoc x dynctx))))
          end
        | _ -> failwith "Not a Dynamic Context"
    end
  | DynCtx _ -> failwith "Cannot translate Dynamic Context"
  | Let _ -> failwith "Lets need to already have been desugared"

let rec translate_to_static expr = 
  match expr with 
  | Int n -> fun ctx -> Int n
  | Var x -> 
    fun ctx -> begin 
        match List.assoc_opt x ctx with 
        | Some value -> value 
        | None -> failwith("Unbound Variable Name " ^ x ^ " in Lambda Term.")
      end 
  | App(e1, e2) -> begin 
      fun ctx -> 
        App(translate_to_static e1 ctx, translate_to_static e2 ctx)
    end
  | Abs(x, e) -> begin 
      let v = gen_new_var () in 
      fun ctx -> 
        Abs(v, translate_to_static e ((x, Var(v))::(List.remove_assoc x ctx)))
    end
  | Plus(e1, e2) -> begin 
      fun ctx -> 
        Plus(translate_to_static e1 ctx, translate_to_static e2 ctx)
    end
  | Let _ -> failwith "Lets need to already have been desugared"
  | DynCtx _ -> failwith "No Dynamic Context Handling"

let main = 
  (* let prog = 
     Let("x", Int(3),
        Let("f", Abs("y", Plus(Var("x"), Var("y"))), 
            Let("x1", Int(5), 
                App(Var("f"), Var("x1"))))) in  *)
  (* let prog = Let("x", Int(3), Var("x")) in  *)
  (* let prog = 
     Let("x", Int(3),
        Let("f", Abs("y", Plus(Var("x"), Var("y"))), 
            App(Var("f"), Var("x")))) in  *)
  (* let prog = 
     Let("f", Abs("y", Plus(Int(2), Var("y"))), 
        App(Var("f"), Int(3))) in  *)
  let prog = 
    Let("x", Int(3),
        Let("f", Abs("y", Plus(Var("x"), Var("y"))), 
            Let("x", Int(5), 
                Let("g", Abs("z", Let("x", App(Var("f"), Var("x")), App(Var("f"), Var("x")))),
                    Let("x", Int(7), 
                        Let("y", Int(9),
                            Plus(App(Var("g"), Var("y")), App(Var("f"), Var("x"))))))))) in 
  let prog' = remove_lets prog in 
  let dynamic = translate_to_dynamic prog' (DynCtx([])) in 
  let () = dynamic |> expr_to_str |> print_endline in 
  let end_val = eval dynamic true in 
  end_val |> val_to_str |> print_endline