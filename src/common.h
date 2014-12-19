#pragma GCC diagnostic ignored "-Wunused-result"

#ifndef _COMMON_H_
#define _COMMON_H_

#define flag { printf("\nLINE: %d\n", __LINE__); fflush(stdout); }

#include <vector>
#include <cmath>

struct Problem
{
    Problem(uint32_t const nr_instance, uint32_t const nr_feature, uint64_t const range_sum)
          :nr_instance(nr_instance), nr_feature(nr_feature), range_sum(range_sum),  
          J(static_cast<uint64_t>(nr_instance) * nr_feature, range_sum), 
          Y(nr_instance){}
    uint32_t nr_instance, nr_feature;
    uint64_t range_sum;
    std::vector<uint64_t> J; 
    std::vector<float> Y; 
};

Problem read_tr_problem(std::string const tr_path, std::map<std::pair<uint32_t, uint32_t>, uint64_t> &fviMap);

Problem read_va_problem(std::string const va_path, std::map<std::pair<uint32_t, uint32_t>, uint64_t> &fviMap, uint64_t const range_sum, uint32_t const nr_feature);

uint32_t const kW_NODE_SIZE = 2;

struct Model
{
    Model(uint64_t const range_sum, uint32_t const nr_factor) 
        : range_sum(range_sum), nr_factor(nr_factor),
        W(range_sum * nr_factor * kW_NODE_SIZE, 0) {} 
    uint64_t range_sum;
    uint32_t nr_factor;
    std::vector<float> W;
};

FILE *open_c_file(std::string const &path, std::string const &mode);

std::vector<std::string> 
argv_to_args(int const argc, char const * const * const argv);

inline float wTx(Problem const &prob, Model &model, uint32_t const i, 
    float const kappa=0, float const eta=0, float const lambda=0, 
    bool const do_update=false)
{
    uint32_t const nr_feature = prob.nr_feature;
    uint64_t const range_sum = prob.range_sum; 
    uint32_t const nr_factor = model.nr_factor;
    uint32_t const align = nr_factor * kW_NODE_SIZE; // +align: next feature value

    //initialize pointers
    uint64_t const * const J = &prob.J[i * nr_feature]; 
    float * const W = model.W.data();

    float predict = 0.0;

    for(uint32_t d = 0; d < nr_factor; d++)
    {
        if(do_update)
        {
            float gs = 0.0;
            for(uint32_t f = 0; f < nr_feature; f++)
            {
                uint64_t const j = J[f];
                if(j >= range_sum) //ignore if not present in training set
                    continue;
                gs += *(W + j * align + d); // \sum W_{J[f]}_d
            }
            for(uint32_t f = 0; f < nr_feature; f++)
            {
                uint64_t const j = J[f];
                if(j >= range_sum) //ignore if not present in training set
                    continue;
                float * const w = W + j * align + d;  
                float * const shg = w + nr_factor;
                float const gradient = kappa * (gs - *w) + lambda * *w; //compute gradient
                *shg += (gradient * gradient); //update sum history gradient
                *w -= static_cast<float> (eta * gradient / sqrt(*shg)); //update weight
            }
        }
        else
        {
            for(uint32_t f1 = 0; f1 < nr_feature; f1++)
            {
                uint64_t const j1 = J[f1];
                if(j1 >= range_sum)
                    continue;
                float * const w1 = W + j1 * align + d; 
                for(uint32_t f2 = f1 + 1; f2 < nr_feature; f2++)
                {
                    uint64_t const j2 = J[f2]; 
                    if(j2 >= range_sum)
                        continue;
                    float * const w2 = W + j2 * align + d; 
                    //predict += (*w1) * (*w2) / static_cast<float>(nr_feature); 
                    predict += (*w1) * (*w2);
                }
            }
        }
    }

    if(do_update)
        return 0;
    return predict;
}

float predict(Problem const &prob, Model &model, 
    std::string const &output_path = std::string(""));
#endif // _COMMON_H_
