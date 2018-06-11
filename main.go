package main

import (
	"fmt"
	"log"
	"os"
	"image/color"
	"image"
	"image/png"
)
// Based on:
// https://esolangs.org/wiki/Bitwise_Cyclic_Tag

func bct(data []int, prog []int, limit int) int {
	l := len(prog)
	
	// Program bit pointer:
	p := 0

	var i int
	for i = 0; len(data) > 0 && i < limit; i++ {
		cmd := prog[p]
		p = (p + 1) % l
		if cmd == 0 {
			//fmt.Printf("data=%v cmd=0\n", data)
			data = data[1:]
		} else {
			x := prog[p]
			//fmt.Printf("data=%v cmd=1%d\n", data, x)
			p = (p + 1) % l
			if data[0] == 1 {
				data = append(data, x)
			}
		}
		
	}

	return i
}

func self_bct_2(prog1 []int, prog2 []int, limit int) (bool, int) {
	
	// Program bit pointer:
	p1 := 0
	p2 := 0

	i := 0
	
	for ; len(prog1) > 0 && len(prog2) > 0 && i < limit; i++ {

		cmd1 := prog1[p1]
		if cmd1 == 0 {
			//fmt.Printf("cmd1=0, p1(%d)=%v p2(%d)=%v\n", p1, prog1, p2, prog2)
			p1 = (p1 + 1) % len(prog1)
			prog2 = prog2[1:]
			if len(prog2) == 0 {
				break
			}

			p2 = (p2 + len(prog2) - 1) % len(prog2)
		} else {
			x := prog1[(p1 + 1) % len(prog1)]
			//fmt.Printf("cmd1=1%d, p1(%d)=%v p2(%d)=%v\n", x, p1, prog1, p2, prog2)
			p1 = (p1 + 2) % len(prog1)
			if prog2[0] == 1 {
				prog2 = append(prog2, x)
			}
		}

		cmd2 := prog2[p2]
		if cmd2 == 1 {
			//fmt.Printf("cmd2=0, p1(%d)=%v p2(%d)=%v\n", p1, prog1, p2, prog2)
			p2 = (p2 + 1) % len(prog2)
			prog1 = prog1[1:]

			if len(prog1) == 0 {
				break
			}
			
			p1 = (p1 + len(prog1) - 1) % len(prog1)
		} else {
			x := prog2[(p2 + 1) % len(prog2)]
			//fmt.Printf("cmd2=1%d, p1(%d)=%v p2(%d)=%v\n", x, p1, prog1, p2, prog2)
			p2 = (p2 + 2) % len(prog2)
			if prog1[0] == 0 {
				prog1 = append(prog1, x)
			}
		}
	}

	return len(prog1) == 0 || len(prog2) == 0, i
}

// I mis-read and wrote this thinking it would produce Gray codes, but
// actually it converts *from* Gray codes...
func from_gray_code(bits *[]int) []int {

	gray := make([]int, len(*bits))
	x := 0
	l := len(*bits) - 1
	for i := l; i >= 0; i-- {
		x ^= (*bits)[i]
		gray[i] = x
	}
	return gray
}

func gray_code(bits *[]int) []int {
	gray := make([]int, len(*bits))
	m := len(*bits) - 1
	for i := 0; i < m; i++ {
		gray[i] = (*bits)[i] ^ (*bits)[i + 1]
	}
	gray[m] = (*bits)[m]
	return gray
}

func increment(bits *[]int) bool {
	l := len(*bits)
	i := 0
	b := 0
	for i,b = range *bits {
		if b == 0 {
			(*bits)[i] = 1
			break
		} else {
			(*bits)[i] = 0
		}
	}
	return i == l - 1 && (*bits)[i] == 0
}

func b2i(bits *[]int) int {
	v := 0
	m := 1
	for _,b := range *bits {
		v += b*m
		m <<= 1
	}
	return v
}

func reverse(l *[]int) {
    for i, j := 0, len(*l)-1; i < j; i, j = i+1, j-1 {
        (*l)[i], (*l)[j] = (*l)[j], (*l)[i]
    }
}

func main() {

	size := uint(10)

	img := image.NewRGBA(image.Rect(0, 0, 1 << size, 1 << size))

	var g1 []int
	var g2 []int

	n_halt := 0
	steps_sum := 0
	steps_max := 0
	
	b1 := make([]int, size)
	for more1 := true; more1; more1 = !increment(&b1) {
		g1 = gray_code(&b1)
		b2 := make([]int, size)
		
		for more2 := true; more2; more2 = !increment(&b2) {
			g2 = gray_code(&b2)
			/*
			halt, steps := self_bct_2(g1, g2, 1000)
			if halt {
				n_halt++
				steps_sum += steps
				if steps > steps_max {
					steps_max = steps
				}
			}
            */
			// Not especially interesting:
			// steps := bct(g1, g2, 255)
			//_, steps2 := self_bct_2(b1, b2, 255)
			//reverse(&g1)
			//reverse(&g2)
			x1 := b2i(&g1)
			x2 := b2i(&g2)
			//fmt.Printf("%d %d (%v=%v %v=%v): %v %v %s\n", x1, x2, b1, g1, b2, g2, steps, steps2)
			h := uint8(0)
			s := uint8(0)
			/*
			if halt {
				h = 255
				s = uint8(255 * (steps - int(size)) / 40)
			}
            */
			for _,b := range b1 {
				h += uint8(b)
			}
			for _,b := range b2 {
				s += uint8(b)
			}
			c := color.RGBA {
				h * 10,
				s * 10,
				s * 10,
				255,
			}
			img.Set(x1, x2, c)
		}
	}

	steps_avg := float32(steps_sum) / float32(n_halt)
	fmt.Printf("Average halt time: %.1f\n", steps_avg)
	fmt.Printf("Max halt time: %d\n", steps_max)
	
	//f, err := os.Create("selfbct2_rev_graycode_1024.png")
	f, err := os.Create("binary_ones.png")
	if err != nil {
		log.Fatal(err)
	}

	if err := png.Encode(f, img); err != nil {
		f.Close()
		log.Fatal(err)
	}

	if err := f.Close(); err != nil {
		log.Fatal(err)
	}	
	
	/*
	data := []int{1, 0, 1, 0}
	prog := []int{0, 0, 1, 1, 1}

	//bct(data, prog)
	self_bct_2(data, prog)
    */
}
