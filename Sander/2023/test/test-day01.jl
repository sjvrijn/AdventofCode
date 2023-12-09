using AdventofCode: day01

@testset "Day 1" begin

    @testset "Day 1, part 1" begin
        testfiles = Dict(
            "input01-test1.txt" => 142,
            "input01-test2.txt" => 209,
        )
        for (file, result) in testfiles
            data = readlines(joinpath(INPUT, file))
            @test day01.a(data) == result
        end
    end

    @testset "Day 1, part 2" begin
        testfiles = Dict(
            "input01-test1.txt" => 142,
            "input01-test2.txt" => 281,
        )
        for (file, result) in testfiles
            data = readlines(joinpath(INPUT, file))
            @test day01.b(data) == result
        end
    end

end