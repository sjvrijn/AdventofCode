using Test

const INPUT = joinpath(@__DIR__, "../inputs")

tests = 1:7
if !isempty(ARGS)
	tests = ARGS  # Set list to same as command line args
end

for t in tests
    include("test-day$(lpad(t,2,'0')).jl")
end