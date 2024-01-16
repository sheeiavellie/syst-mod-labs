package main

import (
	"fmt"
	"math"
	"math/rand"
)

const (
	Lambda = 5.0  // Интенсивность потока заявок
	Nu     = 0.5  // Производительность канала
	Error  = 0.01 // Допустимая абсолютная погрешность
)

var bigT []float64

func deltaT(randNum float64) float64 {
	return -math.Log(1-randNum) / Lambda
}

func deltaTau(randNum float64) float64 {
	return -math.Log(randNum) / Nu
}

func processRequests(time float64, NStar int) (int, int) {
	rand.New(rand.NewSource(21))
	M := 0
	N := 0
	t := 0.0

	for t < time || N < NStar {

		randomNumber := rand.Float64()
		ti := deltaT(randomNumber)

		if t == 0.0 {
			N += 1
			M += 1
			t = ti
		} else {
			t += ti
			N += 1
			randomNumber = rand.Float64()
			taui := deltaTau(randomNumber)

			if ti >= taui {
				M += 1
			}
		}
		bigT = append(bigT, ti)
	}

	return M, N
}

func processError(alphaD int, pAStar float64, N int) float64 {
	return float64(alphaD) * math.Sqrt((pAStar*(1-pAStar))/float64(N))
}

func main() {
	bigT = make([]float64, 15000) //mb too much
	time := 100.0
	M := 0
	N := 0
	NStar := 0
	alphaD := 3

	fmt.Println("Вероятность обслуживания: ", Nu/(Nu+Lambda))
	fmt.Println("Вероятность отказа: ", Lambda/(Nu+Lambda))

	for {
		if N != 0 {
			fmt.Println("Доп. серия опытов N = ", NStar, ":")
		}
		mCur, nCur := processRequests(time, NStar)
		N += nCur
		M += mCur

		fmt.Println("Кол-во заявок на вход: ", N)
		fmt.Println("Кол-во обслуженных заявок: ", M)

		pStar := float64(M) / float64(N)
		fmt.Println("Вероятность обслуживания: ", pStar)

		qStar := (float64(N) - float64(M)) / float64(N)
		fmt.Println("Вероятность отказа: ", qStar)

		errVal := processError(alphaD, float64(qStar), N)
		fmt.Println("Погрешность результата: ", errVal)

		if errVal <= Error {
			break
		}

		NAsked := math.Pow(float64(alphaD), 2.0) * float64(qStar) * (1 - float64(qStar)) * (1.0 / math.Pow(Error, 2.0))
		fmt.Println("Требуемое количество опытов: ", NAsked)

		sum := 0.0
		for _, e := range bigT {
			sum += e
		}
		lStar := float64(N) / sum
		fmt.Println("Интенсивность: ", lStar)

		fmt.Println("Необходимое время моделирования: ", NAsked/lStar)

		fmt.Println("Введите объем дополнительной серии опытов:")
		_, err := fmt.Scanf("%d", &NStar)
		if err != nil {
			fmt.Println(err, ": Incorrect input error")
		}
		fmt.Println("")
	}
}
