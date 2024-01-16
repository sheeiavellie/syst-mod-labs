package main

import "fmt"

type MooreMachine struct {
	States     []string
	Inputs     []string
	Outputs    []string
	TransTable map[string]map[string]string
	CurState   string
}

func NewMooreMachine(
	states,
	inputs,
	outputs []string,
	transTable map[string]map[string]string,
	initialState string,
) *MooreMachine {
	return &MooreMachine{
		States:     states,
		Inputs:     inputs,
		Outputs:    outputs,
		TransTable: transTable,
		CurState:   initialState,
	}
}

func (m *MooreMachine) Transition(input string) {
	fmt.Println("Вход:", input)

	nextState, ok := m.TransTable[m.CurState][input]
	if !ok {
		fmt.Println("Некорректный вход:", input)
		return
	}

	m.CurState = nextState
	fmt.Println("Текущее состояние:", m.CurState)
	fmt.Println("Выход:", m.TransTable[m.CurState]["output"])
}

var initState string
var input string

func main() {
	states := []string{"S0", "S1", "S2", "S3", "S4", "S5"}
	inputs := []string{"I0", "I1", "I2", "I3", "I4", "I5"}
	outputs := []string{"O0", "O1", "O2", "O3"}

	transTable := map[string]map[string]string{
		"S0": {"I0": "S1", "I1": "S2", "I2": "S3", "I3": "S4", "I4": "S5", "I5": "S0", "output": "O0"},
		"S1": {"I0": "S2", "I1": "S3", "I2": "S4", "I3": "S5", "I4": "S0", "I5": "S1", "output": "O1"},
		"S2": {"I0": "S3", "I1": "S4", "I2": "S5", "I3": "S0", "I4": "S1", "I5": "S2", "output": "O2"},
		"S3": {"I0": "S4", "I1": "S5", "I2": "S0", "I3": "S1", "I4": "S2", "I5": "S3", "output": "O3"},
		"S4": {"I0": "S5", "I1": "S0", "I2": "S1", "I3": "S2", "I4": "S3", "I5": "S4", "output": "O0"},
		"S5": {"I0": "S0", "I1": "S1", "I2": "S2", "I3": "S3", "I4": "S4", "I5": "S5", "output": "O1"},
	}

	fmt.Print("Введите начальное состояние: ")
	_, err := fmt.Scanf("%s", &initState)
	if err != nil {
		fmt.Println(err, ": Incorrect input error")
	}
	mooreMachine := NewMooreMachine(states, inputs, outputs, transTable, initState)

	for {
		fmt.Print("Введите вход или q для выхода: ")
		_, err := fmt.Scanf("%s", &input)
		if err != nil {
			fmt.Println(err, ": Incorrect input error")
		}

		if input == "q" {
			break
		}

		mooreMachine.Transition(input)
	}
}
